#!/usr/bin/env python3
import redis
import json
import subprocess
import os
import tempfile
import logging
import time
import threading
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import queue
import signal
import sys
from minio import Minio
from minio.error import S3Error

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ManimProcessor:
    def __init__(self, redis_host='redis', redis_port=6379, max_workers=4, 
                 minio_host='minio:9000', minio_access_key='minioadmin', 
                 minio_secret_key='minioadmin', bucket_name='manim-storage'):
        """Initialize the Manim processor with Redis and MinIO connections."""
        self.redis_client = redis.Redis(
            host=redis_host, 
            port=redis_port, 
            decode_responses=True
        )
        
        # Initialize MinIO client
        self.minio_client = Minio(
            minio_host,
            access_key=minio_access_key,
            secret_key=minio_secret_key,
            secure=False  # Set to True if using HTTPS
        )
        self.bucket_name = bucket_name
        
        self.output_dir = Path('/app/outputs')
        self.temp_dir = Path('/app/temp')
        self.max_workers = max_workers
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.running = True
        
        # Create directories if they don't exist
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.temp_dir.mkdir(parents=True, exist_ok=True)
        
        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        
        logger.info(f"Initialized ManimProcessor with Redis at {redis_host}:{redis_port}")
        logger.info(f"MinIO configured at {minio_host} with bucket '{bucket_name}'")
        logger.info(f"Max concurrent workers: {max_workers}")
        
        # Initialize MinIO bucket
        self._init_minio_bucket()
    
    def _init_minio_bucket(self):
        """Initialize MinIO bucket if it doesn't exist."""
        try:
            if not self.minio_client.bucket_exists(self.bucket_name):
                self.minio_client.make_bucket(self.bucket_name)
                logger.info(f"Created MinIO bucket: {self.bucket_name}")
            else:
                logger.info(f"MinIO bucket '{self.bucket_name}' already exists")
        except Exception as e:
            logger.error(f"Failed to initialize MinIO bucket: {e}")
            raise
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully."""
        logger.info(f"Received signal {signum}, shutting down gracefully...")
        self.running = False
        self.executor.shutdown(wait=True)
        sys.exit(0)
    
    def test_redis_connection(self):
        """Test if Redis connection is working."""
        try:
            self.redis_client.ping()
            logger.info("Redis connection successful")
            return True
        except Exception as e:
            logger.error(f"Redis connection failed: {e}")
            return False
    
    def upload_to_minio(self, file_path, user_id, presentation_id, slide_id, file_type):
        """Upload file to MinIO and return the object path."""
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                logger.error(f"File not found: {file_path}")
                return None
            
            # Create object path: user_id/presentation_id/slide_id/video or image
            file_extension = file_path.suffix
            object_name = f"{user_id}/{presentation_id}/{slide_id}/{file_type}{file_extension}"
            
            # Upload file
            self.minio_client.fput_object(
                bucket_name=self.bucket_name,
                object_name=object_name,
                file_path=str(file_path)
            )
            
            # Generate URL (adjust based on your MinIO setup)
            url = f"http://minio:9000/{self.bucket_name}/{object_name}"
            logger.info(f"Uploaded {file_type} to MinIO: {url}")
            return url
            
        except S3Error as e:
            logger.error(f"MinIO S3 error uploading {file_type}: {e}")
            return None
        except Exception as e:
            logger.error(f"Error uploading {file_type} to MinIO: {e}")
            return None

    def process_manim_code(self, manim_code, user_id, presentation_id, slide_id):
        """Process the Manim code and return both video and image paths."""
        thread_id = threading.current_thread().ident
        logger.info(f"[Thread-{thread_id}] Processing request for {user_id}/{presentation_id}/{slide_id}")
        
        temp_file = None
        try:
            # Create a unique filename with thread ID for better uniqueness
            timestamp = int(time.time() * 1000)  # milliseconds for better uniqueness
            filename = f"{user_id}_{presentation_id}_{slide_id}_{timestamp}_{thread_id}"
            temp_file = self.temp_dir / f"{filename}.py"
            
            # Write the Manim code to a temporary file
            with open(temp_file, 'w') as f:
                f.write(manim_code)
            
            logger.info(f"[Thread-{thread_id}] Created temp file: {temp_file}")
            
            # Render video first
            video_path = self._render_video(temp_file, thread_id)
            
            # Render image
            image_path = self._render_image(temp_file, thread_id)
            
            results = {}
            
            # Upload video to MinIO if successful
            if video_path:
                video_url = self.upload_to_minio(video_path, user_id, presentation_id, slide_id, "video")
                results['video_path'] = video_url
                results['video_local'] = str(video_path)
            
            # Upload image to MinIO if successful
            if image_path:
                image_url = self.upload_to_minio(image_path, user_id, presentation_id, slide_id, "image")
                results['image_path'] = image_url
                results['image_local'] = str(image_path)
            
            # Clean up temp file
            if temp_file and temp_file.exists():
                temp_file.unlink()
            
            return results if results else None
                
        except Exception as e:
            logger.error(f"[Thread-{thread_id}] Error processing Manim code: {e}")
            return None
        finally:
            # Clean up temp file
            if temp_file and temp_file.exists():
                try:
                    temp_file.unlink()
                except Exception as e:
                    logger.warning(f"[Thread-{thread_id}] Failed to clean up temp file: {e}")
    
    def _render_video(self, temp_file, thread_id):
        """Render video using Manim."""
        try:
            # Run Manim command for video
            cmd = [
                'manim',
                str(temp_file),
                '-qh',  # high quality video
                '--media_dir', str(self.output_dir),
            ]
            
            logger.info(f"[Thread-{thread_id}] Running video command: {' '.join(cmd)}")
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=1200  # 20 minutes
            )
            
            if result.returncode == 0:
                # Find the generated video file
                scene_name = self.extract_scene_name(open(temp_file).read())
                video_dir = self.output_dir / 'videos' / temp_file.stem / '1080p60'
                
                if video_dir.exists():
                    video_files = list(video_dir.glob('*.mp4'))
                    if video_files:
                        logger.info(f"[Thread-{thread_id}] Video generated: {video_files[0]}")
                        return str(video_files[0])
                
                logger.error(f"[Thread-{thread_id}] Video file not found after successful execution")
                return None
            else:
                logger.error(f"[Thread-{thread_id}] Video rendering failed: {result.stderr}")
                return None
                
        except subprocess.TimeoutExpired:
            logger.error(f"[Thread-{thread_id}] Video rendering timed out")
            return None
        except Exception as e:
            logger.error(f"[Thread-{thread_id}] Error rendering video: {e}")
            return None
    
    def _render_image(self, temp_file, thread_id):
        """Render image using Manim."""
        try:
            # Run Manim command for image
            cmd = [
                'manim',
                str(temp_file),
                '-s',  # save last frame as image
                '--media_dir', str(self.output_dir),
            ]
            
            logger.info(f"[Thread-{thread_id}] Running image command: {' '.join(cmd)}")
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=1200  # 20 minutes for image
            )
            
            if result.returncode == 0:
                # Find the generated image file
                scene_name = self.extract_scene_name(open(temp_file).read())
                image_dir = self.output_dir / 'images' / temp_file.stem
                
                if image_dir.exists():
                    image_files = list(image_dir.glob('*.png'))
                    if image_files:
                        logger.info(f"[Thread-{thread_id}] Image generated: {image_files[0]}")
                        return str(image_files[0])
                
                logger.error(f"[Thread-{thread_id}] Image file not found after successful execution")
                return None
            else:
                logger.error(f"[Thread-{thread_id}] Image rendering failed: {result.stderr}")
                return None
                
        except subprocess.TimeoutExpired:
            logger.error(f"[Thread-{thread_id}] Image rendering timed out")
            return None
        except Exception as e:
            logger.error(f"[Thread-{thread_id}] Error rendering image: {e}")
            return None
    
    def extract_scene_name(self, manim_code):
        """Extract scene class name from Manim code."""
        lines = manim_code.split('\n')
        for line in lines:
            if 'class ' in line and '(Scene)' in line:
                # Extract class name
                class_line = line.strip()
                class_name = class_line.split('class ')[1].split('(')[0].strip()
                return class_name
        return 'Scene'  # Default fallback
    
    def send_response(self, original_data, results):
        """Send response back to kaari:render:out channel."""
        thread_id = threading.current_thread().ident
        try:
            response_data = {
                "user_id": original_data["user_id"],
                "presentation_id": original_data["presentation_id"],
                "slide_id": original_data["slide_id"],
                "status": "success" if results else "error"
            }
            
            if results:
                response_data.update(results)
            
            response_json = json.dumps(response_data)
            self.redis_client.publish('kaari:render:out', response_json)
            logger.info(f"[Thread-{thread_id}] Response sent to kaari:render:out {response_json}")
            
        except Exception as e:
            logger.error(f"[Thread-{thread_id}] Error sending response: {e}")
    
    def process_message_async(self, data):
        """Process a single message asynchronously."""
        thread_id = threading.current_thread().ident
        try:
            logger.info(f"[Thread-{thread_id}] Processing message: {data}")
            
            # Extract required fields
            user_id = data.get('user_id')
            presentation_id = data.get('presentation_id')
            slide_id = data.get('slide_id')
            manim_code = data.get('manim_code')
            
            if not all([user_id, presentation_id, slide_id, manim_code]):
                logger.error(f"[Thread-{thread_id}] Missing required fields in message")
                self.send_response(data, None)
                return
            
            # Process the Manim code
            results = self.process_manim_code(
                manim_code, user_id, presentation_id, slide_id
            )
            
            # Send response
            self.send_response(data, results)
            
        except Exception as e:
            logger.error(f"[Thread-{thread_id}] Error processing message: {e}")
            self.send_response(data, None)
    
    def listen_and_process(self):
        """Main loop to listen for messages and process them concurrently."""
        logger.info("Starting to listen on kaari:render:in channel...")
        
        pubsub = self.redis_client.pubsub()
        pubsub.subscribe('kaari:render:in')
        
        # Skip the subscription confirmation message
        for message in pubsub.listen():
            if message['type'] == 'subscribe':
                logger.info(f"Successfully subscribed to {message['channel']}")
                continue
                
            if not self.running:
                break
                
            if message['type'] == 'message':
                try:
                    # Parse the JSON data
                    data = json.loads(message['data'])
                    
                    # Submit the task to the thread pool
                    future = self.executor.submit(self.process_message_async, data)
                    
                    # Log the submission
                    logger.info(f"Submitted message to worker pool: {data.get('user_id', 'unknown')}/{data.get('slide_id', 'unknown')}")
                    
                except json.JSONDecodeError as e:
                    logger.error(f"Failed to parse JSON: {e}")
                except Exception as e:
                    logger.error(f"Error submitting message to worker pool: {e}")
        
        # Cleanup
        pubsub.close()
        self.executor.shutdown(wait=True)
        logger.info("Service stopped")

    def get_stats(self):
        """Get current processing statistics."""
        return {
            "max_workers": self.max_workers,
            "active_threads": threading.active_count(),
            "running": self.running
        }

def main():
    """Main function to run the processor."""
    # Get configuration from environment variables
    max_workers = int(os.environ.get('MANIM_MAX_WORKERS', '2'))
    minio_host = os.environ.get('MINIO_HOST', 'minio:9000')
    minio_access_key = os.environ.get('MINIO_ACCESS_KEY', 'minioadmin')
    minio_secret_key = os.environ.get('MINIO_SECRET_KEY', 'minioadmin')
    bucket_name = os.environ.get('MINIO_BUCKET', 'manim-storage')
    
    processor = ManimProcessor(
        max_workers=max_workers,
        minio_host=minio_host,
        minio_access_key=minio_access_key,
        minio_secret_key=minio_secret_key,
        bucket_name=bucket_name
    )
    
    # Test Redis connection before starting
    if not processor.test_redis_connection():
        logger.error("Failed to connect to Redis. Exiting...")
        return
    
    # Log initial stats
    stats = processor.get_stats()
    logger.info(f"Service starting with stats: {stats}")
    
    # Start listening and processing
    try:
        processor.listen_and_process()
    except KeyboardInterrupt:
        logger.info("Received interrupt signal, shutting down...")
    except Exception as e:
        logger.error(f"Fatal error in main loop: {e}")
    finally:
        processor.executor.shutdown(wait=True)
        logger.info("Service shutdown complete")

if __name__ == "__main__":
    main()