# ClassZero Application Documentation

## Overview
ClassZero is a presentation management and editing application built with Python and CustomTkinter. It provides a user-friendly interface for creating, editing, and managing presentations with various media types.

## Features

### 1. User Authentication
- Secure login system with email/password
- Session management
- User-specific presentation access

### 2. Presentation Management
- Create and manage multiple presentations
- View presentation list with details
- Open presentations in editor mode

### 3. Slide Editor
- Create and edit slides with rich content
- Support for various media types (images, videos)
- Real-time preview
- Slide organization and reordering

### 4. Presentation Mode
- Full-screen presentation view
- Slide navigation controls
- Timer and presenter notes

## Technical Architecture

### Backend
- **Database**: PostgreSQL for persistent storage
- **Caching**: Redis for improved performance
- **API**: RESTful endpoints for data operations

### Frontend
- Built with CustomTkinter for modern UI
- Responsive design for various screen sizes
- Dark/Light theme support

## Project Structure

```
app/
├── app_main.py          # Main application entry point
├── app_login.py         # User authentication module
├── app_editor.py        # Main editor interface
├── app_presentations_list.py  # Presentation list view
├── app_editor_*.py      # Editor submodules:
│   ├── app_editor_dbm.py     # Database manager
│   ├── app_editor_ol.py      # Loading overlay
│   ├── app_editor_vp.py      # Video player
│   ├── app_editor_sc.py      # Slide card component
│   ├── app_editor_nsd.py     # New slide dialog
│   └── app_editor_pm.py      # Presentation mode
├── globals.css          # Global styles
├── layout.tsx           # Application layout
└── page.tsx             # Main page component
```

## Dependencies

### Core Dependencies
- Python 3.8+
- CustomTkinter
- psycopg2 (PostgreSQL adapter)
- redis-py
- OpenCV (for media processing)
- Pillow (for image processing)
- Requests (for HTTP requests)
- imageio (for video processing)

### Database
- PostgreSQL 13+
- Redis 6.0+

## Setup Instructions

### Prerequisites
1. Install Python 3.8 or higher
2. Install PostgreSQL and create a database named 'ClassZero'
3. Install Redis server

### Installation
1. Clone the repository
2. Install Python dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Configure database connection in `HostPortMapping.py`
4. Run the application:
   ```
   python app/app_main.py
   ```

## Usage

1. **Login**
   - Launch the application
   - Enter your credentials
   - Click "Sign In"

2. **Manage Presentations**
   - View your presentations in the list
   - Create new presentations
   - Open existing presentations for editing

3. **Edit Presentation**
   - Add/remove slides
   - Add content (text, images, videos)
   - Reorder slides
   - Save changes

4. **Present**
   - Enter presentation mode
   - Navigate through slides
   - Use presenter tools

## Security Considerations

- Passwords are hashed before storage
- Secure session management
- Input validation on all forms
- Database connection pooling

## Troubleshooting

### Common Issues
1. **Connection Errors**
   - Verify database server is running
   - Check connection parameters in `HostPortMapping.py`
   - Ensure proper network connectivity

2. **Media Loading Issues**
   - Verify file paths
   - Check file permissions
   - Ensure supported file formats

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2025 ClassZero

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
