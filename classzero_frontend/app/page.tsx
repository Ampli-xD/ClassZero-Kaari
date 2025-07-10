"use client"

import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import {
  Download,
  Github,
  Code,
  Video,
  Cpu,
  Database,
  Settings,
  ArrowRight,
  PlayCircle,
  ExternalLink,
  Terminal,
  Zap,
  Shield,
  Monitor,
  Copy,
  Table,
  GitBranch,
  HelpCircle,
  Quote,
  Info,
  ImageIcon,
} from "lucide-react"
import Link from "next/link"

export default function KaariPremiumDark() {
  const scrollToInstallation = () => {
    document.getElementById("installation")?.scrollIntoView({ behavior: "smooth" })
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950 text-white">
      {/* Navigation */}
      <nav className="fixed top-0 w-full bg-slate-950/80 backdrop-blur-xl border-b border-slate-800/50 z-50">
        <div className="container mx-auto px-4 sm:px-6 h-16 flex items-center justify-between">
          <div className="flex items-center space-x-2 sm:space-x-3">
            <div className="w-8 h-8 sm:w-9 sm:h-9 bg-gradient-to-br from-cyan-400 to-blue-600 rounded-xl flex items-center justify-center shadow-lg shadow-cyan-500/25">
              <span className="text-white font-bold text-sm sm:text-lg">C</span>
            </div>
            <div className="flex items-center space-x-1 sm:space-x-2">
              <span className="text-lg sm:text-2xl font-bold bg-gradient-to-r from-white to-slate-300 bg-clip-text text-transparent">
                ClassZero
              </span>
              <div className="text-slate-400 text-sm sm:text-lg">/</div>
              <span className="text-sm sm:text-xl font-semibold text-cyan-400">Kaari</span>
            </div>
          </div>
          <div className="hidden md:flex items-center space-x-8">
            <Link href="#features" className="text-slate-300 hover:text-cyan-400 transition-colors duration-200">
              Features
            </Link>
            <Link href="#demos" className="text-slate-300 hover:text-cyan-400 transition-colors duration-200">
              Demos
            </Link>
            <Link href="#architecture" className="text-slate-300 hover:text-cyan-400 transition-colors duration-200">
              Architecture
            </Link>
            <Link href="#installation" className="text-slate-300 hover:text-cyan-400 transition-colors duration-200">
              Installation
            </Link>
          </div>
          <div className="flex items-center space-x-2 sm:space-x-3">
            <Button
              variant="outline"
              size="sm"
              className="border-slate-600 bg-slate-800/50 hover:bg-slate-700/50 text-slate-300 hidden sm:flex"
            >
              <Github className="w-4 h-4 mr-2" />
              Repository
            </Button>
            <Button
              size="sm"
              onClick={scrollToInstallation}
              className="bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 shadow-lg shadow-cyan-500/25"
            >
              <Download className="w-4 h-4 mr-1 sm:mr-2" />
              <span className="hidden sm:inline">Install</span>
            </Button>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="pt-24 sm:pt-32 pb-16 sm:pb-20 px-4 sm:px-6">
        <div className="container mx-auto max-w-7xl">
          <div className="grid lg:grid-cols-2 gap-8 lg:gap-16 items-center">
            <div className="space-y-6 sm:space-y-8">
              <div className="space-y-4 sm:space-y-6">
                <Badge className="bg-gradient-to-r from-cyan-500/20 to-blue-600/20 text-cyan-400 border-cyan-500/30 px-3 sm:px-4 py-1 sm:py-2 text-xs sm:text-sm">
                  🚀 AI-Powered Desktop Application
                </Badge>
                <h1 className="text-3xl sm:text-5xl md:text-6xl lg:text-7xl font-bold leading-tight">
                  <span className="bg-gradient-to-r from-white via-slate-200 to-slate-400 bg-clip-text text-transparent">
                    AI-Powered
                  </span>
                  <br />
                  <span className="bg-gradient-to-r from-cyan-400 via-blue-500 to-purple-600 bg-clip-text text-transparent">
                    Slide Creation
                  </span>
                  <br />
                  <span className="bg-gradient-to-r from-white via-slate-200 to-slate-400 bg-clip-text text-transparent">
                    & Presentation
                  </span>
                </h1>
                <p className="text-lg sm:text-xl text-slate-300 leading-relaxed max-w-2xl">
                  Transform your teaching concepts into professional presentation slides with AI precision. Create
                  tables, flowcharts, questions, quotes, and more with presentation mode built-in.
                </p>
              </div>

              <div className="flex flex-col sm:flex-row gap-3 sm:gap-4">
                <Button
                  size="lg"
                  onClick={scrollToInstallation}
                  className="bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 text-base sm:text-lg px-6 sm:px-8 py-4 sm:py-6 shadow-lg shadow-cyan-500/25"
                >
                  <Github className="w-4 sm:w-5 h-4 sm:h-5 mr-2" />
                  Install from GitHub
                </Button>
                <Button
                  size="lg"
                  variant="outline"
                  className="border-slate-600 bg-slate-800/50 hover:bg-slate-700/50 text-base sm:text-lg px-6 sm:px-8 py-4 sm:py-6"
                >
                  <PlayCircle className="w-4 sm:w-5 h-4 sm:h-5 mr-2" />
                  View Demo Videos
                </Button>
              </div>

              <div className="flex flex-wrap items-center gap-4 sm:gap-8 text-xs sm:text-sm text-slate-400">
                <div className="flex items-center space-x-2">
                  <Shield className="w-3 sm:w-4 h-3 sm:h-4 text-green-400" />
                  <span>100% Local Control</span>
                </div>
                <div className="flex items-center space-x-2">
                  <Code className="w-3 sm:w-4 h-3 sm:h-4 text-cyan-400" />
                  <span>Open Source</span>
                </div>
                <div className="flex items-center space-x-2">
                  <Monitor className="w-3 sm:w-4 h-3 sm:h-4 text-purple-400" />
                  <span>Windows Desktop</span>
                </div>
              </div>
            </div>

            <div className="relative mt-8 lg:mt-0">
              <div className="absolute inset-0 bg-gradient-to-r from-cyan-500/20 to-blue-600/20 rounded-2xl sm:rounded-3xl blur-2xl sm:blur-3xl"></div>
              <div className="relative bg-gradient-to-br from-slate-800 to-slate-900 rounded-xl sm:rounded-2xl p-4 sm:p-8 border border-slate-700/50 shadow-2xl">
                <div className="bg-slate-950 rounded-lg sm:rounded-xl p-4 sm:p-6 space-y-4 sm:space-y-6">
                  <div className="flex items-center space-x-2 text-xs sm:text-sm text-slate-400">
                    <div className="w-2 sm:w-3 h-2 sm:h-3 bg-red-500 rounded-full"></div>
                    <div className="w-2 sm:w-3 h-2 sm:h-3 bg-yellow-500 rounded-full"></div>
                    <div className="w-2 sm:w-3 h-2 sm:h-3 bg-green-500 rounded-full"></div>
                    <span className="ml-2 font-mono text-xs sm:text-sm">Kaari Desktop v1.0</span>
                  </div>
                  <div className="space-y-3 sm:space-y-4">
                    <div className="bg-slate-800/50 rounded-lg p-3 sm:p-4 border border-slate-700/30">
                      <p className="text-xs sm:text-sm text-slate-400 mb-2">Query Input:</p>
                      <p className="font-mono text-xs sm:text-sm text-cyan-400">
                        "Explain photosynthesis with animated molecular diagrams"
                      </p>
                    </div>
                    <div className="flex justify-center">
                      <div className="flex items-center space-x-2 text-cyan-400">
                        <ArrowRight className="w-4 sm:w-5 h-4 sm:h-5 animate-pulse" />
                        <span className="text-xs sm:text-sm font-mono">Processing...</span>
                      </div>
                    </div>
                    <div className="bg-gradient-to-r from-green-900/30 to-blue-900/30 rounded-lg p-3 sm:p-4 border border-green-500/20">
                      <div className="flex items-center space-x-2 mb-3">
                        <Monitor className="w-3 sm:w-4 h-3 sm:h-4 text-green-400" />
                        <span className="text-xs sm:text-sm font-medium text-green-400">Generated Slides</span>
                        <Badge variant="outline" className="text-xs border-green-500/30 text-green-400">
                          12 slides • Presentation Mode
                        </Badge>
                      </div>
                      <div className="bg-slate-900 rounded-lg aspect-video flex items-center justify-center border border-slate-700/30">
                        <div className="text-center space-y-2">
                          <div className="grid grid-cols-3 gap-1 sm:gap-2 w-16 sm:w-24">
                            <div className="w-4 sm:w-6 h-3 sm:h-4 bg-cyan-400/30 rounded"></div>
                            <div className="w-4 sm:w-6 h-3 sm:h-4 bg-purple-400/30 rounded"></div>
                            <div className="w-4 sm:w-6 h-3 sm:h-4 bg-orange-400/30 rounded"></div>
                            <div className="w-4 sm:w-6 h-3 sm:h-4 bg-green-400/30 rounded"></div>
                            <div className="w-4 sm:w-6 h-3 sm:h-4 bg-blue-400/30 rounded"></div>
                            <div className="w-4 sm:w-6 h-3 sm:h-4 bg-pink-400/30 rounded"></div>
                          </div>
                          <p className="text-xs sm:text-sm text-slate-400">Photosynthesis Slides</p>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Key Features */}
      <section id="features" className="py-16 sm:py-20 px-4 sm:px-6">
        <div className="container mx-auto max-w-7xl">
          <div className="text-center space-y-4 mb-12 sm:mb-16">
            <h2 className="text-3xl sm:text-4xl md:text-5xl font-bold bg-gradient-to-r from-white to-slate-300 bg-clip-text text-transparent">
              Professional Educational Content Creation
            </h2>
            <p className="text-lg sm:text-xl text-slate-400 max-w-3xl mx-auto">
              Built with cutting-edge technology for educators who demand excellence
            </p>
          </div>

          <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6 sm:gap-8">
            <Card className="bg-gradient-to-br from-slate-800 to-slate-900 border-slate-700/50 hover:border-cyan-500/30 transition-all duration-300 group">
              <CardHeader className="p-4 sm:p-6">
                <div className="w-12 sm:w-14 h-12 sm:h-14 bg-gradient-to-br from-cyan-500/20 to-blue-600/20 rounded-xl flex items-center justify-center mb-4 group-hover:scale-110 transition-transform duration-300">
                  <Zap className="w-6 sm:w-7 h-6 sm:h-7 text-cyan-400" />
                </div>
                <CardTitle className="text-white text-lg sm:text-xl">Multiple Slide Types</CardTitle>
                <CardDescription className="text-slate-400 text-sm sm:text-base">
                  Create tables, flowcharts, questions, quotes, info slides, images, and more with AI assistance
                </CardDescription>
              </CardHeader>
            </Card>

            <Card className="bg-gradient-to-br from-slate-800 to-slate-900 border-slate-700/50 hover:border-purple-500/30 transition-all duration-300 group">
              <CardHeader className="p-4 sm:p-6">
                <div className="w-12 sm:w-14 h-12 sm:h-14 bg-gradient-to-br from-purple-500/20 to-pink-600/20 rounded-xl flex items-center justify-center mb-4 group-hover:scale-110 transition-transform duration-300">
                  <Monitor className="w-6 sm:w-7 h-6 sm:h-7 text-purple-400" />
                </div>
                <CardTitle className="text-white text-lg sm:text-xl">Presentation Mode</CardTitle>
                <CardDescription className="text-slate-400 text-sm sm:text-base">
                  Built-in presentation mode for seamless delivery of your AI-generated educational content
                </CardDescription>
              </CardHeader>
            </Card>

            <Card className="bg-gradient-to-br from-slate-800 to-slate-900 border-slate-700/50 hover:border-green-500/30 transition-all duration-300 group">
              <CardHeader className="p-4 sm:p-6">
                <div className="w-12 sm:w-14 h-12 sm:h-14 bg-gradient-to-br from-green-500/20 to-emerald-600/20 rounded-xl flex items-center justify-center mb-4 group-hover:scale-110 transition-transform duration-300">
                  <Shield className="w-6 sm:w-7 h-6 sm:h-7 text-green-400" />
                </div>
                <CardTitle className="text-white text-lg sm:text-xl">Local Installation</CardTitle>
                <CardDescription className="text-slate-400 text-sm sm:text-base">
                  Complete control over your educational content with local desktop deployment
                </CardDescription>
              </CardHeader>
            </Card>

            <Card className="bg-gradient-to-br from-slate-800 to-slate-900 border-slate-700/50 hover:border-orange-500/30 transition-all duration-300 group">
              <CardHeader className="p-4 sm:p-6">
                <div className="w-12 sm:w-14 h-12 sm:h-14 bg-gradient-to-br from-orange-500/20 to-red-600/20 rounded-xl flex items-center justify-center mb-4 group-hover:scale-110 transition-transform duration-300">
                  <Database className="w-6 sm:w-7 h-6 sm:h-7 text-orange-400" />
                </div>
                <CardTitle className="text-white text-lg sm:text-xl">Microservices Architecture</CardTitle>
                <CardDescription className="text-slate-400 text-sm sm:text-base">
                  Scalable architecture with Redis, MinIO, n8n, and HAProxy for institutional deployments
                </CardDescription>
              </CardHeader>
            </Card>

            <Card className="bg-gradient-to-br from-slate-800 to-slate-900 border-slate-700/50 hover:border-blue-500/30 transition-all duration-300 group">
              <CardHeader className="p-4 sm:p-6">
                <div className="w-12 sm:w-14 h-12 sm:h-14 bg-gradient-to-br from-blue-500/20 to-indigo-600/20 rounded-xl flex items-center justify-center mb-4 group-hover:scale-110 transition-transform duration-300">
                  <Monitor className="w-6 sm:w-7 h-6 sm:h-7 text-blue-400" />
                </div>
                <CardTitle className="text-white text-lg sm:text-xl">Windows Desktop</CardTitle>
                <CardDescription className="text-slate-400 text-sm sm:text-base">
                  Native Tkinter interface designed for professional educational workflows
                </CardDescription>
              </CardHeader>
            </Card>

            <Card className="bg-gradient-to-br from-slate-800 to-slate-900 border-slate-700/50 hover:border-cyan-500/30 transition-all duration-300 group">
              <CardHeader className="p-4 sm:p-6">
                <div className="w-12 sm:w-14 h-12 sm:h-14 bg-gradient-to-br from-cyan-500/20 to-teal-600/20 rounded-xl flex items-center justify-center mb-4 group-hover:scale-110 transition-transform duration-300">
                  <Code className="w-6 sm:w-7 h-6 sm:h-7 text-cyan-400" />
                </div>
                <CardTitle className="text-white text-lg sm:text-xl">Open Source</CardTitle>
                <CardDescription className="text-slate-400 text-sm sm:text-base">
                  Transparent development with full access to source code and community contributions
                </CardDescription>
              </CardHeader>
            </Card>
          </div>
        </div>
      </section>

      {/* Demo Slide Types Section */}
      <section id="demos" className="py-16 sm:py-20 px-4 sm:px-6 bg-slate-900/50">
        <div className="container mx-auto max-w-7xl">
          <div className="text-center space-y-4 mb-12 sm:mb-16">
            <h2 className="text-3xl sm:text-4xl md:text-5xl font-bold bg-gradient-to-r from-white to-slate-300 bg-clip-text text-transparent">
              See Different Slide Types
            </h2>
            <p className="text-lg sm:text-xl text-slate-400 max-w-3xl mx-auto">
              Explore the variety of slide types Kaari can generate for your presentations
            </p>
          </div>

          <Tabs defaultValue="tables" className="w-full">
            <TabsList className="grid grid-cols-3 sm:grid-cols-6 mb-8 sm:mb-12 bg-slate-800/50 border border-slate-700/50 h-auto p-1">
              <TabsTrigger
                value="tables"
                className="data-[state=active]:bg-cyan-500/20 data-[state=active]:text-cyan-400 text-xs sm:text-sm py-2"
              >
                Tables
              </TabsTrigger>
              <TabsTrigger
                value="flowcharts"
                className="data-[state=active]:bg-green-500/20 data-[state=active]:text-green-400 text-xs sm:text-sm py-2"
              >
                Flowcharts
              </TabsTrigger>
              <TabsTrigger
                value="questions"
                className="data-[state=active]:bg-purple-500/20 data-[state=active]:text-purple-400 text-xs sm:text-sm py-2"
              >
                Questions
              </TabsTrigger>
              <TabsTrigger
                value="quotes"
                className="data-[state=active]:bg-orange-500/20 data-[state=active]:text-orange-400 text-xs sm:text-sm py-2"
              >
                Quotes
              </TabsTrigger>
              <TabsTrigger
                value="info"
                className="data-[state=active]:bg-blue-500/20 data-[state=active]:text-blue-400 text-xs sm:text-sm py-2"
              >
                Info
              </TabsTrigger>
              <TabsTrigger
                value="images"
                className="data-[state=active]:bg-pink-500/20 data-[state=active]:text-pink-400 text-xs sm:text-sm py-2"
              >
                Images
              </TabsTrigger>
            </TabsList>

            <TabsContent value="tables" className="space-y-6 sm:space-y-8">
              <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6 sm:gap-8">
                <Card className="bg-gradient-to-br from-slate-800 to-slate-900 border-slate-700/50 overflow-hidden group hover:border-cyan-500/30 transition-all duration-300">
                  <div className="aspect-video bg-slate-950 flex items-center justify-center border-b border-slate-700/50">
                    <div className="text-center space-y-3">
                      <Table className="w-12 h-12 text-cyan-400 mx-auto group-hover:scale-110 transition-transform duration-300" />
                      <Badge variant="outline" className="border-cyan-500/30 text-cyan-400 text-xs">
                        Data Table
                      </Badge>
                    </div>
                  </div>
                  <CardContent className="p-4">
                    <div className="space-y-2">
                      <Badge className="bg-cyan-500/20 text-cyan-400 border-cyan-500/30 text-xs">Comparison</Badge>
                      <p className="text-sm text-slate-300 font-mono">
                        "Create a comparison table of renewable energy sources"
                      </p>
                    </div>
                  </CardContent>
                </Card>

                <Card className="bg-gradient-to-br from-slate-800 to-slate-900 border-slate-700/50 overflow-hidden group hover:border-cyan-500/30 transition-all duration-300">
                  <div className="aspect-video bg-slate-950 flex items-center justify-center border-b border-slate-700/50">
                    <div className="text-center space-y-3">
                      <Table className="w-12 h-12 text-cyan-400 mx-auto group-hover:scale-110 transition-transform duration-300" />
                      <Badge variant="outline" className="border-cyan-500/30 text-cyan-400 text-xs">
                        Statistics Table
                      </Badge>
                    </div>
                  </div>
                  <CardContent className="p-4">
                    <div className="space-y-2">
                      <Badge className="bg-cyan-500/20 text-cyan-400 border-cyan-500/30 text-xs">Mathematics</Badge>
                      <p className="text-sm text-slate-300 font-mono">
                        "Show probability distributions in tabular format"
                      </p>
                    </div>
                  </CardContent>
                </Card>

                <Card className="bg-gradient-to-br from-slate-800 to-slate-900 border-slate-700/50 overflow-hidden group hover:border-cyan-500/30 transition-all duration-300">
                  <div className="aspect-video bg-slate-950 flex items-center justify-center border-b border-slate-700/50">
                    <div className="text-center space-y-3">
                      <Table className="w-12 h-12 text-cyan-400 mx-auto group-hover:scale-110 transition-transform duration-300" />
                      <Badge variant="outline" className="border-cyan-500/30 text-cyan-400 text-xs">
                        Schedule Table
                      </Badge>
                    </div>
                  </div>
                  <CardContent className="p-4">
                    <div className="space-y-2">
                      <Badge className="bg-cyan-500/20 text-cyan-400 border-cyan-500/30 text-xs">Planning</Badge>
                      <p className="text-sm text-slate-300 font-mono">"Create a weekly study schedule table"</p>
                    </div>
                  </CardContent>
                </Card>
              </div>
            </TabsContent>

            <TabsContent value="flowcharts" className="space-y-6 sm:space-y-8">
              <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6 sm:gap-8">
                <Card className="bg-gradient-to-br from-slate-800 to-slate-900 border-slate-700/50 overflow-hidden group hover:border-green-500/30 transition-all duration-300">
                  <div className="aspect-video bg-slate-950 flex items-center justify-center border-b border-slate-700/50">
                    <div className="text-center space-y-3">
                      <GitBranch className="w-12 h-12 text-green-400 mx-auto group-hover:scale-110 transition-transform duration-300" />
                      <Badge variant="outline" className="border-green-500/30 text-green-400 text-xs">
                        Process Flow
                      </Badge>
                    </div>
                  </div>
                  <CardContent className="p-4">
                    <div className="space-y-2">
                      <Badge className="bg-green-500/20 text-green-400 border-green-500/30 text-xs">Biology</Badge>
                      <p className="text-sm text-slate-300 font-mono">"Photosynthesis process flowchart with steps"</p>
                    </div>
                  </CardContent>
                </Card>

                <Card className="bg-gradient-to-br from-slate-800 to-slate-900 border-slate-700/50 overflow-hidden group hover:border-green-500/30 transition-all duration-300">
                  <div className="aspect-video bg-slate-950 flex items-center justify-center border-b border-slate-700/50">
                    <div className="text-center space-y-3">
                      <GitBranch className="w-12 h-12 text-green-400 mx-auto group-hover:scale-110 transition-transform duration-300" />
                      <Badge variant="outline" className="border-green-500/30 text-green-400 text-xs">
                        Decision Tree
                      </Badge>
                    </div>
                  </div>
                  <CardContent className="p-4">
                    <div className="space-y-2">
                      <Badge className="bg-green-500/20 text-green-400 border-green-500/30 text-xs">Logic</Badge>
                      <p className="text-sm text-slate-300 font-mono">"Problem-solving decision flowchart"</p>
                    </div>
                  </CardContent>
                </Card>

                <Card className="bg-gradient-to-br from-slate-800 to-slate-900 border-slate-700/50 overflow-hidden group hover:border-green-500/30 transition-all duration-300">
                  <div className="aspect-video bg-slate-950 flex items-center justify-center border-b border-slate-700/50">
                    <div className="text-center space-y-3">
                      <GitBranch className="w-12 h-12 text-green-400 mx-auto group-hover:scale-110 transition-transform duration-300" />
                      <Badge variant="outline" className="border-green-500/30 text-green-400 text-xs">
                        Algorithm Flow
                      </Badge>
                    </div>
                  </div>
                  <CardContent className="p-4">
                    <div className="space-y-2">
                      <Badge className="bg-green-500/20 text-green-400 border-green-500/30 text-xs">Programming</Badge>
                      <p className="text-sm text-slate-300 font-mono">"Sorting algorithm step-by-step flowchart"</p>
                    </div>
                  </CardContent>
                </Card>
              </div>
            </TabsContent>

            <TabsContent value="questions" className="space-y-6 sm:space-y-8">
              <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6 sm:gap-8">
                <Card className="bg-gradient-to-br from-slate-800 to-slate-900 border-slate-700/50 overflow-hidden group hover:border-purple-500/30 transition-all duration-300">
                  <div className="aspect-video bg-slate-950 flex items-center justify-center border-b border-slate-700/50">
                    <div className="text-center space-y-3">
                      <HelpCircle className="w-12 h-12 text-purple-400 mx-auto group-hover:scale-110 transition-transform duration-300" />
                      <Badge variant="outline" className="border-purple-500/30 text-purple-400 text-xs">
                        Multiple Choice
                      </Badge>
                    </div>
                  </div>
                  <CardContent className="p-4">
                    <div className="space-y-2">
                      <Badge className="bg-purple-500/20 text-purple-400 border-purple-500/30 text-xs">Quiz</Badge>
                      <p className="text-sm text-slate-300 font-mono">
                        "Create multiple choice questions about history"
                      </p>
                    </div>
                  </CardContent>
                </Card>

                <Card className="bg-gradient-to-br from-slate-800 to-slate-900 border-slate-700/50 overflow-hidden group hover:border-purple-500/30 transition-all duration-300">
                  <div className="aspect-video bg-slate-950 flex items-center justify-center border-b border-slate-700/50">
                    <div className="text-center space-y-3">
                      <HelpCircle className="w-12 h-12 text-purple-400 mx-auto group-hover:scale-110 transition-transform duration-300" />
                      <Badge variant="outline" className="border-purple-500/30 text-purple-400 text-xs">
                        Open Ended
                      </Badge>
                    </div>
                  </div>
                  <CardContent className="p-4">
                    <div className="space-y-2">
                      <Badge className="bg-purple-500/20 text-purple-400 border-purple-500/30 text-xs">
                        Discussion
                      </Badge>
                      <p className="text-sm text-slate-300 font-mono">"Generate discussion questions for literature"</p>
                    </div>
                  </CardContent>
                </Card>

                <Card className="bg-gradient-to-br from-slate-800 to-slate-900 border-slate-700/50 overflow-hidden group hover:border-purple-500/30 transition-all duration-300">
                  <div className="aspect-video bg-slate-950 flex items-center justify-center border-b border-slate-700/50">
                    <div className="text-center space-y-3">
                      <HelpCircle className="w-12 h-12 text-purple-400 mx-auto group-hover:scale-110 transition-transform duration-300" />
                      <Badge variant="outline" className="border-purple-500/30 text-purple-400 text-xs">
                        True/False
                      </Badge>
                    </div>
                  </div>
                  <CardContent className="p-4">
                    <div className="space-y-2">
                      <Badge className="bg-purple-500/20 text-purple-400 border-purple-500/30 text-xs">
                        Assessment
                      </Badge>
                      <p className="text-sm text-slate-300 font-mono">"True/false questions about scientific facts"</p>
                    </div>
                  </CardContent>
                </Card>
              </div>
            </TabsContent>

            <TabsContent value="quotes" className="space-y-6 sm:space-y-8">
              <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6 sm:gap-8">
                <Card className="bg-gradient-to-br from-slate-800 to-slate-900 border-slate-700/50 overflow-hidden group hover:border-orange-500/30 transition-all duration-300">
                  <div className="aspect-video bg-slate-950 flex items-center justify-center border-b border-slate-700/50">
                    <div className="text-center space-y-3">
                      <Quote className="w-12 h-12 text-orange-400 mx-auto group-hover:scale-110 transition-transform duration-300" />
                      <Badge variant="outline" className="border-orange-500/30 text-orange-400 text-xs">
                        Inspirational
                      </Badge>
                    </div>
                  </div>
                  <CardContent className="p-4">
                    <div className="space-y-2">
                      <Badge className="bg-orange-500/20 text-orange-400 border-orange-500/30 text-xs">
                        Motivation
                      </Badge>
                      <p className="text-sm text-slate-300 font-mono">"Famous quotes about education and learning"</p>
                    </div>
                  </CardContent>
                </Card>

                <Card className="bg-gradient-to-br from-slate-800 to-slate-900 border-slate-700/50 overflow-hidden group hover:border-orange-500/30 transition-all duration-300">
                  <div className="aspect-video bg-slate-950 flex items-center justify-center border-b border-slate-700/50">
                    <div className="text-center space-y-3">
                      <Quote className="w-12 h-12 text-orange-400 mx-auto group-hover:scale-110 transition-transform duration-300" />
                      <Badge variant="outline" className="border-orange-500/30 text-orange-400 text-xs">
                        Historical
                      </Badge>
                    </div>
                  </div>
                  <CardContent className="p-4">
                    <div className="space-y-2">
                      <Badge className="bg-orange-500/20 text-orange-400 border-orange-500/30 text-xs">History</Badge>
                      <p className="text-sm text-slate-300 font-mono">"Important historical quotes with context"</p>
                    </div>
                  </CardContent>
                </Card>

                <Card className="bg-gradient-to-br from-slate-800 to-slate-900 border-slate-700/50 overflow-hidden group hover:border-orange-500/30 transition-all duration-300">
                  <div className="aspect-video bg-slate-950 flex items-center justify-center border-b border-slate-700/50">
                    <div className="text-center space-y-3">
                      <Quote className="w-12 h-12 text-orange-400 mx-auto group-hover:scale-110 transition-transform duration-300" />
                      <Badge variant="outline" className="border-orange-500/30 text-orange-400 text-xs">
                        Scientific
                      </Badge>
                    </div>
                  </div>
                  <CardContent className="p-4">
                    <div className="space-y-2">
                      <Badge className="bg-orange-500/20 text-orange-400 border-orange-500/30 text-xs">Science</Badge>
                      <p className="text-sm text-slate-300 font-mono">"Famous scientific quotes and discoveries"</p>
                    </div>
                  </CardContent>
                </Card>
              </div>
            </TabsContent>

            <TabsContent value="info" className="space-y-6 sm:space-y-8">
              <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6 sm:gap-8">
                <Card className="bg-gradient-to-br from-slate-800 to-slate-900 border-slate-700/50 overflow-hidden group hover:border-blue-500/30 transition-all duration-300">
                  <div className="aspect-video bg-slate-950 flex items-center justify-center border-b border-slate-700/50">
                    <div className="text-center space-y-3">
                      <Info className="w-12 h-12 text-blue-400 mx-auto group-hover:scale-110 transition-transform duration-300" />
                      <Badge variant="outline" className="border-blue-500/30 text-blue-400 text-xs">
                        Key Facts
                      </Badge>
                    </div>
                  </div>
                  <CardContent className="p-4">
                    <div className="space-y-2">
                      <Badge className="bg-blue-500/20 text-blue-400 border-blue-500/30 text-xs">Summary</Badge>
                      <p className="text-sm text-slate-300 font-mono">"Key facts about climate change"</p>
                    </div>
                  </CardContent>
                </Card>

                <Card className="bg-gradient-to-br from-slate-800 to-slate-900 border-slate-700/50 overflow-hidden group hover:border-blue-500/30 transition-all duration-300">
                  <div className="aspect-video bg-slate-950 flex items-center justify-center border-b border-slate-700/50">
                    <div className="text-center space-y-3">
                      <Info className="w-12 h-12 text-blue-400 mx-auto group-hover:scale-110 transition-transform duration-300" />
                      <Badge variant="outline" className="border-blue-500/30 text-blue-400 text-xs">
                        Definition
                      </Badge>
                    </div>
                  </div>
                  <CardContent className="p-4">
                    <div className="space-y-2">
                      <Badge className="bg-blue-500/20 text-blue-400 border-blue-500/30 text-xs">Concept</Badge>
                      <p className="text-sm text-slate-300 font-mono">"Define complex mathematical concepts"</p>
                    </div>
                  </CardContent>
                </Card>

                <Card className="bg-gradient-to-br from-slate-800 to-slate-900 border-slate-700/50 overflow-hidden group hover:border-blue-500/30 transition-all duration-300">
                  <div className="aspect-video bg-slate-950 flex items-center justify-center border-b border-slate-700/50">
                    <div className="text-center space-y-3">
                      <Info className="w-12 h-12 text-blue-400 mx-auto group-hover:scale-110 transition-transform duration-300" />
                      <Badge variant="outline" className="border-blue-500/30 text-blue-400 text-xs">
                        Overview
                      </Badge>
                    </div>
                  </div>
                  <CardContent className="p-4">
                    <div className="space-y-2">
                      <Badge className="bg-blue-500/20 text-blue-400 border-blue-500/30 text-xs">Introduction</Badge>
                      <p className="text-sm text-slate-300 font-mono">"Course overview and learning objectives"</p>
                    </div>
                  </CardContent>
                </Card>
              </div>
            </TabsContent>

            <TabsContent value="images" className="space-y-6 sm:space-y-8">
              <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6 sm:gap-8">
                <Card className="bg-gradient-to-br from-slate-800 to-slate-900 border-slate-700/50 overflow-hidden group hover:border-pink-500/30 transition-all duration-300">
                  <div className="aspect-video bg-slate-950 flex items-center justify-center border-b border-slate-700/50">
                    <div className="text-center space-y-3">
                      <ImageIcon className="w-12 h-12 text-pink-400 mx-auto group-hover:scale-110 transition-transform duration-300" />
                      <Badge variant="outline" className="border-pink-500/30 text-pink-400 text-xs">
                        Diagram
                      </Badge>
                    </div>
                  </div>
                  <CardContent className="p-4">
                    <div className="space-y-2">
                      <Badge className="bg-pink-500/20 text-pink-400 border-pink-500/30 text-xs">Visual</Badge>
                      <p className="text-sm text-slate-300 font-mono">"Generate diagrams for complex concepts"</p>
                    </div>
                  </CardContent>
                </Card>

                <Card className="bg-gradient-to-br from-slate-800 to-slate-900 border-slate-700/50 overflow-hidden group hover:border-pink-500/30 transition-all duration-300">
                  <div className="aspect-video bg-slate-950 flex items-center justify-center border-b border-slate-700/50">
                    <div className="text-center space-y-3">
                      <ImageIcon className="w-12 h-12 text-pink-400 mx-auto group-hover:scale-110 transition-transform duration-300" />
                      <Badge variant="outline" className="border-pink-500/30 text-pink-400 text-xs">
                        Illustration
                      </Badge>
                    </div>
                  </div>
                  <CardContent className="p-4">
                    <div className="space-y-2">
                      <Badge className="bg-pink-500/20 text-pink-400 border-pink-500/30 text-xs">Art</Badge>
                      <p className="text-sm text-slate-300 font-mono">
                        "Create educational illustrations and graphics"
                      </p>
                    </div>
                  </CardContent>
                </Card>

                <Card className="bg-gradient-to-br from-slate-800 to-slate-900 border-slate-700/50 overflow-hidden group hover:border-pink-500/30 transition-all duration-300">
                  <div className="aspect-video bg-slate-950 flex items-center justify-center border-b border-slate-700/50">
                    <div className="text-center space-y-3">
                      <ImageIcon className="w-12 h-12 text-pink-400 mx-auto group-hover:scale-110 transition-transform duration-300" />
                      <Badge variant="outline" className="border-pink-500/30 text-pink-400 text-xs">
                        Chart
                      </Badge>
                    </div>
                  </div>
                  <CardContent className="p-4">
                    <div className="space-y-2">
                      <Badge className="bg-pink-500/20 text-pink-400 border-pink-500/30 text-xs">Data</Badge>
                      <p className="text-sm text-slate-300 font-mono">
                        "Visual charts and graphs for data presentation"
                      </p>
                    </div>
                  </CardContent>
                </Card>
              </div>
            </TabsContent>
          </Tabs>
        </div>
      </section>

      {/* Technical Architecture */}
      <section id="architecture" className="py-16 sm:py-20 px-4 sm:px-6">
        <div className="container mx-auto max-w-7xl">
          <div className="text-center space-y-4 mb-12 sm:mb-16">
            <h2 className="text-3xl sm:text-4xl md:text-5xl font-bold bg-gradient-to-r from-white to-slate-300 bg-clip-text text-transparent">
              Technical Architecture
            </h2>
            <p className="text-lg sm:text-xl text-slate-400 max-w-3xl mx-auto">
              Easily setup on a local server in your institution and use it seamlessly across the network
            </p>
          </div>

          <div className="grid lg:grid-cols-2 gap-8 lg:gap-12 items-center mb-12 sm:mb-16">
            <div className="space-y-6 sm:space-y-8">
              <div className="space-y-4">
                <h3 className="text-xl sm:text-2xl font-bold text-white">Institutional Deployment</h3>
                <p className="text-slate-400 leading-relaxed text-sm sm:text-base">
                  Setup Kaari on your local server and provide seamless access across your institution's network.
                  Perfect for schools, universities, and training centers.
                </p>
              </div>
              <div className="space-y-4">
                <h3 className="text-xl sm:text-2xl font-bold text-white">Scalable Microservices</h3>
                <p className="text-slate-400 leading-relaxed text-sm sm:text-base">
                  Built with Redis for caching, MinIO for storage, n8n for workflows, Manim-processor for animations,
                  and HAProxy as reverse proxy and load balancer for horizontal scaling.
                </p>
              </div>
              <div className="space-y-4">
                <h3 className="text-xl sm:text-2xl font-bold text-white">Network-Wide Access</h3>
                <p className="text-slate-400 leading-relaxed text-sm sm:text-base">
                  Once deployed, educators across your network can access Kaari through their desktop applications,
                  sharing resources and maintaining consistent performance.
                </p>
              </div>
            </div>

            <div className="relative">
              <div className="absolute inset-0 bg-gradient-to-r from-cyan-500/10 to-blue-600/10 rounded-xl sm:rounded-2xl blur-xl sm:blur-2xl"></div>
              <div className="relative bg-gradient-to-br from-slate-800 to-slate-900 rounded-xl sm:rounded-2xl p-4 sm:p-8 border border-slate-700/50">
                <div className="space-y-4 sm:space-y-6">
                  <div className="flex items-center justify-between p-3 sm:p-4 bg-slate-950/50 rounded-lg border border-slate-700/30">
                    <div className="flex items-center space-x-2 sm:space-x-3">
                      <Monitor className="w-5 sm:w-6 h-5 sm:h-6 text-cyan-400" />
                      <span className="text-white font-medium text-sm sm:text-base">Desktop Clients</span>
                    </div>
                    <Badge className="bg-cyan-500/20 text-cyan-400 border-cyan-500/30 text-xs">Network</Badge>
                  </div>

                  <div className="flex justify-center">
                    <ArrowRight className="w-5 sm:w-6 h-5 sm:h-6 text-slate-500" />
                  </div>

                  <div className="flex items-center justify-between p-3 sm:p-4 bg-slate-950/50 rounded-lg border border-slate-700/30">
                    <div className="flex items-center space-x-2 sm:space-x-3">
                      <Database className="w-5 sm:w-6 h-5 sm:h-6 text-purple-400" />
                      <span className="text-white font-medium text-sm sm:text-base">HAProxy Load Balancer</span>
                    </div>
                    <Badge className="bg-purple-500/20 text-purple-400 border-purple-500/30 text-xs">Scaling</Badge>
                  </div>

                  <div className="flex justify-center">
                    <ArrowRight className="w-5 sm:w-6 h-5 sm:h-6 text-slate-500" />
                  </div>

                  <div className="grid grid-cols-2 gap-2 sm:gap-3">
                    <div className="p-2 sm:p-3 bg-slate-950/50 rounded border border-slate-700/30 text-center">
                      <span className="text-orange-400 text-xs sm:text-sm font-medium">Redis</span>
                    </div>
                    <div className="p-2 sm:p-3 bg-slate-950/50 rounded border border-slate-700/30 text-center">
                      <span className="text-green-400 text-xs sm:text-sm font-medium">MinIO</span>
                    </div>
                    <div className="p-2 sm:p-3 bg-slate-950/50 rounded border border-slate-700/30 text-center">
                      <span className="text-blue-400 text-xs sm:text-sm font-medium">n8n</span>
                    </div>
                    <div className="p-2 sm:p-3 bg-slate-950/50 rounded border border-slate-700/30 text-center">
                      <span className="text-pink-400 text-xs sm:text-sm font-medium">Manim</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-6">
            <Card className="bg-gradient-to-br from-slate-800 to-slate-900 border-slate-700/50 text-center hover:border-cyan-500/30 transition-all duration-300">
              <CardHeader className="p-4 sm:p-6">
                <div className="w-12 sm:w-16 h-12 sm:h-16 bg-gradient-to-br from-cyan-500/20 to-blue-600/20 rounded-xl sm:rounded-2xl flex items-center justify-center mx-auto mb-3 sm:mb-4">
                  <Settings className="w-6 sm:w-8 h-6 sm:h-8 text-cyan-400" />
                </div>
                <CardTitle className="text-white text-sm sm:text-base">Frontend</CardTitle>
                <CardDescription className="text-slate-400 text-xs sm:text-sm">
                  Custom Tkinter Desktop Interface
                </CardDescription>
              </CardHeader>
            </Card>

            <Card className="bg-gradient-to-br from-slate-800 to-slate-900 border-slate-700/50 text-center hover:border-purple-500/30 transition-all duration-300">
              <CardHeader className="p-4 sm:p-6">
                <div className="w-12 sm:w-16 h-12 sm:h-16 bg-gradient-to-br from-purple-500/20 to-pink-600/20 rounded-xl sm:rounded-2xl flex items-center justify-center mx-auto mb-3 sm:mb-4">
                  <Database className="w-6 sm:w-8 h-6 sm:h-8 text-purple-400" />
                </div>
                <CardTitle className="text-white text-sm sm:text-base">Load Balancer</CardTitle>
                <CardDescription className="text-slate-400 text-xs sm:text-sm">HAProxy Reverse Proxy</CardDescription>
              </CardHeader>
            </Card>

            <Card className="bg-gradient-to-br from-slate-800 to-slate-900 border-slate-700/50 text-center hover:border-orange-500/30 transition-all duration-300">
              <CardHeader className="p-4 sm:p-6">
                <div className="w-12 sm:w-16 h-12 sm:h-16 bg-gradient-to-br from-orange-500/20 to-red-600/20 rounded-xl sm:rounded-2xl flex items-center justify-center mx-auto mb-3 sm:mb-4">
                  <Video className="w-6 sm:w-8 h-6 sm:h-8 text-orange-400" />
                </div>
                <CardTitle className="text-white text-sm sm:text-base">Processing</CardTitle>
                <CardDescription className="text-slate-400 text-xs sm:text-sm">Manim Animation Engine</CardDescription>
              </CardHeader>
            </Card>

            <Card className="bg-gradient-to-br from-slate-800 to-slate-900 border-slate-700/50 text-center hover:border-green-500/30 transition-all duration-300">
              <CardHeader className="p-4 sm:p-6">
                <div className="w-12 sm:w-16 h-12 sm:h-16 bg-gradient-to-br from-green-500/20 to-emerald-600/20 rounded-xl sm:rounded-2xl flex items-center justify-center mx-auto mb-3 sm:mb-4">
                  <Cpu className="w-6 sm:w-8 h-6 sm:h-8 text-green-400" />
                </div>
                <CardTitle className="text-white text-sm sm:text-base">Storage</CardTitle>
                <CardDescription className="text-slate-400 text-xs sm:text-sm">Redis + MinIO + n8n</CardDescription>
              </CardHeader>
            </Card>
          </div>
        </div>
      </section>

      {/* Installation Guide */}
      <section id="installation" className="py-16 sm:py-20 px-4 sm:px-6 bg-slate-900/50">
        <div className="container mx-auto max-w-5xl">
          <div className="text-center space-y-4 mb-12 sm:mb-16">
            <h2 className="text-3xl sm:text-4xl md:text-5xl font-bold bg-gradient-to-r from-white to-slate-300 bg-clip-text text-transparent">
              Installation
            </h2>
            <p className="text-lg sm:text-xl text-slate-400 max-w-3xl mx-auto">
              Get Kaari running on your system with our comprehensive setup guide
            </p>
          </div>

          <div className="space-y-6 sm:space-y-8">
            <div className="flex items-start space-x-4 sm:space-x-6">
              <div className="w-8 sm:w-10 h-8 sm:h-10 bg-gradient-to-br from-cyan-500 to-blue-600 text-white rounded-lg sm:rounded-xl flex items-center justify-center font-bold text-sm sm:text-lg shadow-lg shadow-cyan-500/25 flex-shrink-0">
                1
              </div>
              <div className="flex-1 space-y-3 sm:space-y-4">
                <h3 className="text-lg sm:text-2xl font-semibold text-white">System Requirements</h3>
                <div className="bg-slate-800/50 rounded-lg p-4 sm:p-6 border border-slate-700/50">
                  <div className="grid sm:grid-cols-2 gap-3 sm:gap-4 text-slate-300 text-sm sm:text-base">
                    <div>
                      <p className="font-medium text-cyan-400 mb-2">Operating System:</p>
                      <p>Windows 10/11 (64-bit)</p>
                    </div>
                    <div>
                      <p className="font-medium text-cyan-400 mb-2">Memory:</p>
                      <p>8GB RAM minimum, 16GB recommended</p>
                    </div>
                    <div>
                      <p className="font-medium text-cyan-400 mb-2">Python:</p>
                      <p>Python 3.8+ with pip</p>
                    </div>
                    <div>
                      <p className="font-medium text-cyan-400 mb-2">Docker:</p>
                      <p>Docker Desktop for Windows</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <div className="flex items-start space-x-4 sm:space-x-6">
              <div className="w-8 sm:w-10 h-8 sm:h-10 bg-gradient-to-br from-cyan-500 to-blue-600 text-white rounded-lg sm:rounded-xl flex items-center justify-center font-bold text-sm sm:text-lg shadow-lg shadow-cyan-500/25 flex-shrink-0">
                2
              </div>
              <div className="flex-1 space-y-3 sm:space-y-4">
                <h3 className="text-lg sm:text-2xl font-semibold text-white">Clone Repository</h3>
                <div className="bg-slate-950 rounded-lg p-4 sm:p-6 border border-slate-700/50">
                  <div className="flex items-center justify-between mb-3 sm:mb-4">
                    <span className="text-xs sm:text-sm text-slate-400 font-mono">Terminal</span>
                    <Button
                      size="sm"
                      variant="outline"
                      className="border-slate-600 bg-slate-800/50 hover:bg-slate-700/50 text-slate-300 text-xs sm:text-sm"
                    >
                      <Copy className="w-3 sm:w-4 h-3 sm:h-4 mr-1 sm:mr-2" />
                      Copy
                    </Button>
                  </div>
                  <code className="text-cyan-400 font-mono text-xs sm:text-sm block">
                    git clone https://github.com/ClassZero/kaari.git
                    <br />
                    cd kaari
                  </code>
                </div>
              </div>
            </div>

            <div className="flex items-start space-x-4 sm:space-x-6">
              <div className="w-8 sm:w-10 h-8 sm:h-10 bg-gradient-to-br from-cyan-500 to-blue-600 text-white rounded-lg sm:rounded-xl flex items-center justify-center font-bold text-sm sm:text-lg shadow-lg shadow-cyan-500/25 flex-shrink-0">
                3
              </div>
              <div className="flex-1 space-y-3 sm:space-y-4">
                <h3 className="text-lg sm:text-2xl font-semibold text-white">Install Dependencies</h3>
                <div className="bg-slate-950 rounded-lg p-4 sm:p-6 border border-slate-700/50">
                  <div className="flex items-center justify-between mb-3 sm:mb-4">
                    <span className="text-xs sm:text-sm text-slate-400 font-mono">Terminal</span>
                    <Button
                      size="sm"
                      variant="outline"
                      className="border-slate-600 bg-slate-800/50 hover:bg-slate-700/50 text-slate-300 text-xs sm:text-sm"
                    >
                      <Copy className="w-3 sm:w-4 h-3 sm:h-4 mr-1 sm:mr-2" />
                      Copy
                    </Button>
                  </div>
                  <code className="text-cyan-400 font-mono text-xs sm:text-sm block">
                    pip install -r requirements.txt
                    <br />
                    pip install manim
                  </code>
                </div>
              </div>
            </div>

            <div className="flex items-start space-x-4 sm:space-x-6">
              <div className="w-8 sm:w-10 h-8 sm:h-10 bg-gradient-to-br from-cyan-500 to-blue-600 text-white rounded-lg sm:rounded-xl flex items-center justify-center font-bold text-sm sm:text-lg shadow-lg shadow-cyan-500/25 flex-shrink-0">
                4
              </div>
              <div className="flex-1 space-y-3 sm:space-y-4">
                <h3 className="text-lg sm:text-2xl font-semibold text-white">Setup Docker Services</h3>
                <div className="bg-slate-950 rounded-lg p-4 sm:p-6 border border-slate-700/50">
                  <div className="flex items-center justify-between mb-3 sm:mb-4">
                    <span className="text-xs sm:text-sm text-slate-400 font-mono">Terminal</span>
                    <Button
                      size="sm"
                      variant="outline"
                      className="border-slate-600 bg-slate-800/50 hover:bg-slate-700/50 text-slate-300 text-xs sm:text-sm"
                    >
                      <Copy className="w-3 sm:w-4 h-3 sm:h-4 mr-1 sm:mr-2" />
                      Copy
                    </Button>
                  </div>
                  <code className="text-cyan-400 font-mono text-xs sm:text-sm block">
                    docker-compose up -d
                    <br />
                    docker-compose logs -f
                  </code>
                </div>
              </div>
            </div>

            <div className="flex items-start space-x-4 sm:space-x-6">
              <div className="w-8 sm:w-10 h-8 sm:h-10 bg-gradient-to-br from-cyan-500 to-blue-600 text-white rounded-lg sm:rounded-xl flex items-center justify-center font-bold text-sm sm:text-lg shadow-lg shadow-cyan-500/25 flex-shrink-0">
                5
              </div>
              <div className="flex-1 space-y-3 sm:space-y-4">
                <h3 className="text-lg sm:text-2xl font-semibold text-white">Launch Kaari</h3>
                <div className="bg-slate-950 rounded-lg p-4 sm:p-6 border border-slate-700/50">
                  <div className="flex items-center justify-between mb-3 sm:mb-4">
                    <span className="text-xs sm:text-sm text-slate-400 font-mono">Terminal</span>
                    <Button
                      size="sm"
                      variant="outline"
                      className="border-slate-600 bg-slate-800/50 hover:bg-slate-700/50 text-slate-300 text-xs sm:text-sm"
                    >
                      <Copy className="w-3 sm:w-4 h-3 sm:h-4 mr-1 sm:mr-2" />
                      Copy
                    </Button>
                  </div>
                  <code className="text-cyan-400 font-mono text-xs sm:text-sm">python main.py</code>
                </div>
              </div>
            </div>
          </div>

          <div className="text-center mt-12 sm:mt-16 space-y-4 sm:space-y-6">
            <div className="flex flex-col sm:flex-row gap-3 sm:gap-4 justify-center">
              <Button
                size="lg"
                className="bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 text-base sm:text-lg px-6 sm:px-8 py-4 sm:py-6 shadow-lg shadow-cyan-500/25"
              >
                <Github className="w-4 sm:w-5 h-4 sm:h-5 mr-2" />
                View Full Documentation
              </Button>
              <Button
                size="lg"
                variant="outline"
                className="border-slate-600 bg-slate-800/50 hover:bg-slate-700/50 text-base sm:text-lg px-6 sm:px-8 py-4 sm:py-6"
              >
                <Terminal className="w-4 sm:w-5 h-4 sm:h-5 mr-2" />
                Quick Start Guide
              </Button>
            </div>
            <p className="text-xs sm:text-sm text-slate-400">
              Need help? Check our comprehensive documentation or join the community discussions.
            </p>
          </div>
        </div>
      </section>

      {/* Final CTA */}
      <section className="py-16 sm:py-20 px-4 sm:px-6 bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
        <div className="container mx-auto max-w-5xl text-center">
          <div className="space-y-6 sm:space-y-8">
            <div className="space-y-4">
              <h2 className="text-3xl sm:text-4xl md:text-6xl font-bold bg-gradient-to-r from-white via-cyan-200 to-blue-400 bg-clip-text text-transparent">
                Transform Your Presentations Today
              </h2>
              <p className="text-lg sm:text-xl text-slate-300 max-w-3xl mx-auto leading-relaxed">
                Join the future of educational slide creation. Install Kaari and start generating professional
                presentation slides with multiple formats and built-in presentation mode.
              </p>
            </div>
            <div className="flex flex-col sm:flex-row gap-4 sm:gap-6 justify-center">
              <Button
                size="lg"
                onClick={scrollToInstallation}
                className="bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 text-lg sm:text-xl px-8 sm:px-12 py-6 sm:py-8 shadow-2xl shadow-cyan-500/25"
              >
                <Github className="w-5 sm:w-6 h-5 sm:h-6 mr-2 sm:mr-3" />
                Install from GitHub
              </Button>
              <Button
                size="lg"
                variant="outline"
                className="border-slate-600 bg-slate-800/50 hover:bg-slate-700/50 text-lg sm:text-xl px-8 sm:px-12 py-6 sm:py-8"
              >
                <ExternalLink className="w-5 sm:w-6 h-5 sm:h-6 mr-2 sm:mr-3" />
                View Documentation
              </Button>
            </div>
            <div className="flex flex-wrap items-center justify-center gap-4 sm:gap-8 text-xs sm:text-sm text-slate-400">
              <div className="flex items-center space-x-2">
                <Code className="w-3 sm:w-4 h-3 sm:h-4 text-cyan-400" />
                <span>Open Source</span>
              </div>
              <div className="flex items-center space-x-2">
                <Shield className="w-3 sm:w-4 h-3 sm:h-4 text-green-400" />
                <span>Local Control</span>
              </div>
              <div className="flex items-center space-x-2">
                <Video className="w-3 sm:w-4 h-3 sm:h-4 text-purple-400" />
                <span>Professional Quality</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-slate-950 border-t border-slate-800/50 py-12 sm:py-16 px-4 sm:px-6">
        <div className="container mx-auto max-w-7xl">
          <div className="grid sm:grid-cols-2 md:grid-cols-4 gap-6 sm:gap-8">
            <div className="space-y-4 sm:col-span-2 md:col-span-1">
              <div className="flex items-center space-x-2 sm:space-x-3">
                <div className="w-8 sm:w-9 h-8 sm:h-9 bg-gradient-to-br from-cyan-400 to-blue-600 rounded-xl flex items-center justify-center shadow-lg shadow-cyan-500/25">
                  <span className="text-white font-bold text-sm sm:text-lg">C</span>
                </div>
                <div className="flex items-center space-x-1 sm:space-x-2">
                  <span className="text-lg sm:text-2xl font-bold bg-gradient-to-r from-white to-slate-300 bg-clip-text text-transparent">
                    ClassZero
                  </span>
                  <div className="text-slate-400 text-sm sm:text-base">/</div>
                  <span className="text-sm sm:text-lg font-semibold text-cyan-400">Kaari</span>
                </div>
              </div>
              <p className="text-slate-400 leading-relaxed text-sm sm:text-base">
                Professional AI-powered slide creation and presentation tool from the ClassZero Suite.
              </p>
              <div className="flex flex-wrap items-center gap-2 sm:gap-4">
                <Badge className="bg-cyan-500/20 text-cyan-400 border-cyan-500/30 text-xs">Open Source</Badge>
                <Badge className="bg-green-500/20 text-green-400 border-green-500/30 text-xs">Local Control</Badge>
              </div>
            </div>

            <div className="space-y-4">
              <h4 className="font-semibold text-white text-base sm:text-lg">Product</h4>
              <div className="space-y-2 sm:space-y-3 text-slate-400 text-sm sm:text-base">
                <Link href="#features" className="block hover:text-cyan-400 transition-colors">
                  Features
                </Link>
                <Link href="#demos" className="block hover:text-cyan-400 transition-colors">
                  Demo Videos
                </Link>
                <Link href="#architecture" className="block hover:text-cyan-400 transition-colors">
                  Architecture
                </Link>
                <Link href="#installation" className="block hover:text-cyan-400 transition-colors">
                  Installation
                </Link>
              </div>
            </div>

            <div className="space-y-4">
              <h4 className="font-semibold text-white text-base sm:text-lg">Resources</h4>
              <div className="space-y-2 sm:space-y-3 text-slate-400 text-sm sm:text-base">
                <Link href="#" className="block hover:text-cyan-400 transition-colors">
                  Documentation
                </Link>
                <Link href="#" className="block hover:text-cyan-400 transition-colors">
                  API Reference
                </Link>
                <Link href="#" className="block hover:text-cyan-400 transition-colors">
                  Setup Guide
                </Link>
                <Link href="#" className="block hover:text-cyan-400 transition-colors">
                  Troubleshooting
                </Link>
              </div>
            </div>

            <div className="space-y-4">
              <h4 className="font-semibold text-white text-base sm:text-lg">ClassZero</h4>
              <div className="space-y-2 sm:space-y-3 text-slate-400 text-sm sm:text-base">
                <Link href="#" className="block hover:text-cyan-400 transition-colors">
                  About
                </Link>
                <Link href="#" className="block hover:text-cyan-400 transition-colors">
                  GitHub
                </Link>
                <Link href="#" className="block hover:text-cyan-400 transition-colors">
                  Contact
                </Link>
                <Link href="#" className="block hover:text-cyan-400 transition-colors">
                  Support
                </Link>
              </div>
            </div>
          </div>

          <div className="border-t border-slate-800/50 mt-8 sm:mt-12 pt-6 sm:pt-8 text-center">
            <p className="text-slate-400 text-sm sm:text-base">
              &copy; 2025 ClassZero. Kaari is open source software released under the MIT License.
              Made with love 💙
            </p>
          </div>
        </div>
      </footer>
    </div>
  )
}
