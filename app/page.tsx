'use client'

import { useState } from 'react'
import { Search, BarChart3, FileText, Download, Instagram, Users, Heart, MessageCircle, TrendingUp, Loader2, AlertCircle } from 'lucide-react'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts'

interface ProfileData {
    username: string
    nome_completo: string
    biografia: string
    seguidores: number
    seguindo: number
    total_posts: number
    verificado?: boolean
    is_verified?: boolean
    conta_privada?: boolean
    is_private?: boolean
    url_perfil?: string
    foto_perfil: string
    _mock_data?: boolean
    _mock_reason?: string
    _real_data?: boolean
    posts: Array<{
        id?: string
        legenda?: string
        caption?: string
        curtidas?: number
        likes?: number
        comentarios?: number
        comments?: number
        data_postagem?: string
        date?: string
        tipo?: string
        is_video?: boolean
        url: string
        hashtags?: string[]
    }>
}

interface Metrics {
    engajamento_medio?: string
    taxa_engajamento: number
    posts_semanais?: number
    principais_hashtags?: string[]
    media_curtidas?: number
    media_likes?: number
    media_comentarios?: number
    media_comments?: number
    total_interacoes?: number
    posts_analisados?: number
    melhor_post?: any
}

interface AIReport {
    resumo_negocio?: string
    pontos_fortes?: string
    pontos_fracos?: string
    oportunidades?: string
    sugestao_prospeccao?: string
    [key: string]: any
}

interface AnalysisResult {
    perfil: string
    dados: ProfileData
    metricas: Metrics
    relatorio_ia: AIReport
    status?: string
    data_source?: string
    warning?: string
    cached?: boolean
}

export default function Home() {
    const [username, setUsername] = useState('')
    const [loading, setLoading] = useState(false)
    const [analysis, setAnalysis] = useState<AnalysisResult | null>(null)
    const [error, setError] = useState('')

    // Funções auxiliares para normalizar dados
    const formatNumber = (num: number | undefined | null): string => {
        if (num === undefined || num === null || isNaN(num)) return '0'
        return num.toLocaleString('pt-BR')
    }

    const safeNumber = (num: number | undefined | null, defaultValue: number = 0): number => {
        if (num === undefined || num === null || isNaN(num)) return defaultValue
        return num
    }

    const normalizeMetrics = (metricas: Metrics): Metrics => {
        return {
            ...metricas,
            media_likes: metricas.media_likes ?? metricas.media_curtidas ?? 0,
            media_comentarios: metricas.media_comentarios ?? metricas.media_comments ?? 0,
            taxa_engajamento: metricas.taxa_engajamento ?? 0,
            total_interacoes: metricas.total_interacoes ?? 0,
            posts_analisados: metricas.posts_analisados ?? 0
        }
    }

    const analyzeProfile = async () => {
        if (!username.trim()) {
            setError('Por favor, digite um username válido')
            return
        }

        setLoading(true)
        setError('')
        setAnalysis(null)

        try {
            const cleanUsername = username.replace('@', '').trim()
            const response = await fetch(`http://localhost:8000/analisar/${cleanUsername}`)

            if (response.status === 429) {
                // Rate limiting - tentar com dados mock
                const errorData = await response.json()
                const mockResponse = await fetch(`http://localhost:8000/analisar-mock/${cleanUsername}`)
                if (mockResponse.ok) {
                    const data = await mockResponse.json()
                    data.metricas = normalizeMetrics(data.metricas)
                    setAnalysis(data)
                    setError(`⏱️ Instagram limitando requisições. Aguarde ${Math.ceil(errorData.detail?.retry_after / 60) || 5} minutos. Mostrando dados simulados.`)
                } else {
                    throw new Error('Erro ao analisar perfil')
                }
            } else if (response.status === 403) {
                // Acesso bloqueado
                const errorData = await response.json()
                const mockResponse = await fetch(`http://localhost:8000/analisar-mock/${cleanUsername}`)
                if (mockResponse.ok) {
                    const data = await mockResponse.json()
                    data.metricas = normalizeMetrics(data.metricas)
                    setAnalysis(data)
                    setError(`🚫 Instagram bloqueou o acesso. Aguarde ${Math.ceil(errorData.detail?.retry_after / 60) || 30} minutos. Mostrando dados simulados.`)
                } else {
                    throw new Error('Erro ao analisar perfil')
                }
            } else if (!response.ok) {
                const errorData = await response.json()
                throw new Error(errorData.detail?.message || 'Erro ao analisar perfil')
            } else {
                const data = await response.json()
                
                // Normalizar métricas
                data.metricas = normalizeMetrics(data.metricas)
                
                setAnalysis(data)

                // Mostrar avisos se necessário
                if (data.data_source === 'mock' || data.dados?._mock_data) {
                    const reason = data.dados._mock_reason || data.warning
                    if (reason === 'perfil_nao_encontrado') {
                        setError('⚠️ Perfil não encontrado. Mostrando dados simulados.')
                    } else if (reason === 'erro_instagram') {
                        setError('⚠️ Erro no Instagram. Mostrando dados simulados.')
                    } else if (data.warning) {
                        setError(`⚠️ ${data.warning}`)
                    }
                } else if (data.cached) {
                    setError(`📦 Dados em cache (${data.cache_age_minutes || 0} min atrás)`)
                } else if (data.status === 'partial' || data.dados._partial_data) {
                    setError(`⚠️ Dados parciais: Perfil coletado mas posts indisponíveis devido a bloqueio do Instagram. Métricas de engajamento não disponíveis.`)
                }
            }
        } catch (err) {
            setError('❌ Erro ao analisar perfil. Verifique se o username existe e tente novamente.')
            console.error('Erro:', err)
        } finally {
            setLoading(false)
        }
    }

    const generatePDF = async () => {
        if (!analysis) return

        try {
            const cleanUsername = analysis.dados.username
            const response = await fetch(`http://localhost:8000/gerar-pdf/${cleanUsername}`)

            if (response.ok) {
                const data = await response.json()
                alert(`✅ PDF gerado com sucesso! Local: ${data.pdf_path}`)
            } else {
                alert('❌ Erro ao gerar PDF')
            }
        } catch (err) {
            console.error('Erro ao gerar PDF:', err)
            alert('❌ Erro ao gerar PDF')
        }
    }

    const prepareChartData = () => {
        if (!analysis) return []

        return analysis.dados.posts.slice(0, 12).map((post, index) => {
            const likes = post.curtidas ?? post.likes ?? 0
            const comments = post.comentarios ?? post.comments ?? 0
            
            return {
                name: `Post ${index + 1}`,
                curtidas: likes,
                comentarios: comments,
                engajamento: likes + comments
            }
        })
    }

    const prepareHashtagData = () => {
        if (!analysis) return []

        const hashtagCounts: { [key: string]: number } = {}
        
        analysis.dados.posts.forEach(post => {
            const hashtags = post.hashtags || []
            hashtags.forEach(hashtag => {
                hashtagCounts[hashtag] = (hashtagCounts[hashtag] || 0) + 1
            })
        })

        return Object.entries(hashtagCounts)
            .sort(([, a], [, b]) => b - a)
            .slice(0, 5)
            .map(([hashtag, count]) => ({
                name: hashtag,
                value: count
            }))
    }

    const getEngagementColor = (rate: number): string => {
        if (rate >= 3) return 'text-green-600'
        if (rate >= 1) return 'text-yellow-600'
        return 'text-red-600'
    }

    const getEngagementLabel = (rate: number): string => {
        if (rate >= 3) return 'Excelente'
        if (rate >= 1) return 'Bom'
        if (rate >= 0.5) return 'Regular'
        return 'Baixo'
    }

    const COLORS = ['#E4405F', '#C13584', '#833AB4', '#F56040', '#F77737']

    return (
        <div className="min-h-screen bg-gradient-to-br from-purple-50 via-white to-blue-50">
            {/* Header */}
            <header className="bg-white shadow-lg border-b border-gray-200 sticky top-0 z-50">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
                    <div className="flex items-center justify-between">
                        <div className="flex items-center space-x-3">
                            <Instagram className="h-8 w-8 text-pink-600" />
                            <h1 className="text-2xl font-bold bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent">
                                Analiador de Instagram
                            </h1>
                        </div>
                        <div className="text-sm text-gray-500 flex items-center gap-2">
                            <BarChart3 className="h-4 w-4" />
                            Análise de perfis com IA
                        </div>
                    </div>
                </div>
            </header>

            <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                {/* Search Section */}
                <div className="text-center mb-12">
                    <h2 className="text-4xl font-bold text-gray-900 mb-4">
                        Analise qualquer perfil do Instagram
                    </h2>
                    <p className="text-xl text-gray-600 mb-8">
                        Obtenha insights estratégicos e relatórios detalhados em segundos
                    </p>

                    <div className="max-w-2xl mx-auto">
                        <div className="flex space-x-4">
                            <div className="flex-1">
                                <input
                                    type="text"
                                    placeholder="@username (ex: instagram)"
                                    value={username}
                                    onChange={(e) => setUsername(e.target.value)}
                                    className="w-full px-6 py-4 text-lg border-2 border-gray-300 rounded-xl focus:border-purple-500 focus:outline-none transition-colors shadow-sm"
                                    onKeyPress={(e) => e.key === 'Enter' && analyzeProfile()}
                                />
                            </div>
                            <button
                                onClick={analyzeProfile}
                                disabled={loading}
                                className="px-8 py-4 bg-gradient-to-r from-purple-600 to-pink-600 text-white font-semibold rounded-xl hover:from-purple-700 hover:to-pink-700 transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center space-x-2 shadow-lg"
                            >
                                {loading ? (
                                    <>
                                        <Loader2 className="h-5 w-5 animate-spin" />
                                        <span>Analisando...</span>
                                    </>
                                ) : (
                                    <>
                                        <Search className="h-5 w-5" />
                                        <span>Analisar</span>
                                    </>
                                )}
                            </button>
                        </div>

                        {error && (
                            <div className="mt-4 p-4 bg-yellow-50 border border-yellow-200 rounded-lg flex items-start gap-3">
                                <AlertCircle className="h-5 w-5 text-yellow-600 flex-shrink-0 mt-0.5" />
                                <p className="text-yellow-800 text-sm text-left">{error}</p>
                            </div>
                        )}
                    </div>
                </div>

                {/* Results Section */}
                {analysis && (
                    <div className="space-y-8">
                        {/* Data Source Badge */}
                        {(analysis.data_source === 'mock' || analysis.dados._mock_data) && (
                            <div className="bg-gradient-to-r from-yellow-50 to-orange-50 border-2 border-yellow-300 rounded-xl p-4 flex items-center gap-3">
                                <AlertCircle className="h-6 w-6 text-yellow-600 flex-shrink-0" />
                                <div>
                                    <p className="text-yellow-900 font-semibold">🎭 Modo Demonstração Ativo</p>
                                    <p className="text-yellow-700 text-sm">
                                        Estes são dados simulados para demonstração. Para dados reais, aguarde o rate limiting do Instagram.
                                    </p>
                                </div>
                            </div>
                        )}

                        {/* Profile Overview */}
                        <div className="bg-white rounded-2xl shadow-xl p-8 border border-gray-100">
                            <div className="flex items-start space-x-6">
                                <img
                                    src={analysis.dados.foto_perfil}
                                    alt={analysis.dados.username}
                                    className="w-28 h-28 rounded-full border-4 border-purple-200 shadow-lg"
                                    onError={(e) => {
                                        e.currentTarget.src = 'https://via.placeholder.com/150?text=No+Image'
                                    }}
                                />
                                <div className="flex-1">
                                    <div className="flex items-center space-x-3 mb-2">
                                        <h3 className="text-3xl font-bold text-gray-900">
                                            @{analysis.dados.username}
                                        </h3>
                                        {(analysis.dados.verificado || analysis.dados.is_verified) && (
                                            <span className="bg-blue-100 text-blue-800 text-xs font-semibold px-3 py-1 rounded-full flex items-center gap-1">
                                                ✓ Verificado
                                            </span>
                                        )}
                                        {(analysis.dados.conta_privada || analysis.dados.is_private) && (
                                            <span className="bg-gray-100 text-gray-800 text-xs font-semibold px-3 py-1 rounded-full flex items-center gap-1">
                                                🔒 Privado
                                            </span>
                                        )}
                                    </div>
                                    <p className="text-xl text-gray-600 mb-3">{analysis.dados.nome_completo}</p>
                                    <p className="text-gray-700 mb-4 leading-relaxed">{analysis.dados.biografia || 'Sem biografia'}</p>

                                    <div className="flex space-x-8 text-sm">
                                        <div className="flex items-center space-x-2">
                                            <FileText className="h-5 w-5 text-purple-600" />
                                            <span className="font-bold text-gray-900">{formatNumber(analysis.dados.total_posts)}</span>
                                            <span className="text-gray-600">posts</span>
                                        </div>
                                        <div className="flex items-center space-x-2">
                                            <Users className="h-5 w-5 text-blue-600" />
                                            <span className="font-bold text-gray-900">{formatNumber(analysis.dados.seguidores)}</span>
                                            <span className="text-gray-600">seguidores</span>
                                        </div>
                                        <div className="flex items-center space-x-2">
                                            <Users className="h-5 w-5 text-green-600" />
                                            <span className="font-bold text-gray-900">{formatNumber(analysis.dados.seguindo)}</span>
                                            <span className="text-gray-600">seguindo</span>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>

                        {/* Metrics Cards */}
                        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                            {/* Engagement Rate */}
                            <div className="bg-white rounded-xl shadow-lg p-6 border border-gray-100 hover:shadow-xl transition-shadow">
                                <div className="flex items-center justify-between">
                                    <div>
                                        <p className="text-sm font-medium text-gray-600">Taxa de Engajamento</p>
                                        <p className={`text-3xl font-bold ${getEngagementColor(analysis.metricas.taxa_engajamento)}`}>
                                            {safeNumber(analysis.metricas.taxa_engajamento).toFixed(2)}%
                                        </p>
                                        <p className="text-xs text-gray-500 mt-1">
                                            {getEngagementLabel(analysis.metricas.taxa_engajamento)}
                                        </p>
                                    </div>
                                    <TrendingUp className={`h-10 w-10 ${getEngagementColor(analysis.metricas.taxa_engajamento)}`} />
                                </div>
                            </div>

                            {/* Average Likes */}
                            <div className="bg-white rounded-xl shadow-lg p-6 border border-gray-100 hover:shadow-xl transition-shadow">
                                <div className="flex items-center justify-between">
                                    <div>
                                        <p className="text-sm font-medium text-gray-600">Média Curtidas</p>
                                        <p className="text-3xl font-bold text-gray-900">
                                            {formatNumber(analysis.metricas.media_likes)}
                                        </p>
                                    </div>
                                    <Heart className="h-10 w-10 text-red-500" />
                                </div>
                            </div>

                            {/* Average Comments */}
                            <div className="bg-white rounded-xl shadow-lg p-6 border border-gray-100 hover:shadow-xl transition-shadow">
                                <div className="flex items-center justify-between">
                                    <div>
                                        <p className="text-sm font-medium text-gray-600">Média Comentários</p>
                                        <p className="text-3xl font-bold text-gray-900">
                                            {formatNumber(analysis.metricas.media_comentarios)}
                                        </p>
                                    </div>
                                    <MessageCircle className="h-10 w-10 text-blue-500" />
                                </div>
                            </div>

                            {/* Total Interactions */}
                            <div className="bg-white rounded-xl shadow-lg p-6 border border-gray-100 hover:shadow-xl transition-shadow">
                                <div className="flex items-center justify-between">
                                    <div>
                                        <p className="text-sm font-medium text-gray-600">Total Interações</p>
                                        <p className="text-3xl font-bold text-gray-900">
                                            {formatNumber(analysis.metricas.total_interacoes)}
                                        </p>
                                        <p className="text-xs text-gray-500 mt-1">
                                            {safeNumber(analysis.metricas.posts_analisados)} posts
                                        </p>
                                    </div>
                                    <BarChart3 className="h-10 w-10 text-purple-500" />
                                </div>
                            </div>
                        </div>

                        {/* Charts */}
                        {prepareChartData().length > 0 && (
                            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                                {/* Engagement Chart */}
                                <div className="bg-white rounded-2xl shadow-xl p-6 border border-gray-100">
                                    <h3 className="text-xl font-semibold text-gray-900 mb-6 flex items-center gap-2">
                                        <BarChart3 className="h-5 w-5 text-purple-600" />
                                        Engajamento por Post
                                    </h3>
                                    <ResponsiveContainer width="100%" height={300}>
                                        <BarChart data={prepareChartData()}>
                                            <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                                            <XAxis dataKey="name" tick={{ fontSize: 12 }} />
                                            <YAxis tick={{ fontSize: 12 }} />
                                            <Tooltip 
                                                contentStyle={{ 
                                                    backgroundColor: 'white', 
                                                    border: '1px solid #e0e0e0',
                                                    borderRadius: '8px'
                                                }}
                                            />
                                            <Bar dataKey="engajamento" fill="url(#colorGradient)" radius={[8, 8, 0, 0]} />
                                            <defs>
                                                <linearGradient id="colorGradient" x1="0" y1="0" x2="0" y2="1">
                                                    <stop offset="0%" stopColor="#9333ea" stopOpacity={0.8}/>
                                                    <stop offset="100%" stopColor="#ec4899" stopOpacity={0.8}/>
                                                </linearGradient>
                                            </defs>
                                        </BarChart>
                                    </ResponsiveContainer>
                                </div>

                                {/* Hashtags Chart */}
                                {prepareHashtagData().length > 0 && (
                                    <div className="bg-white rounded-2xl shadow-xl p-6 border border-gray-100">
                                        <h3 className="text-xl font-semibold text-gray-900 mb-6 flex items-center gap-2">
                                            <Hash className="h-5 w-5 text-pink-600" />
                                            Principais Hashtags
                                        </h3>
                                        <ResponsiveContainer width="100%" height={300}>
                                            <PieChart>
                                                <Pie
                                                    data={prepareHashtagData()}
                                                    cx="50%"
                                                    cy="50%"
                                                    labelLine={false}
                                                    label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                                                    outerRadius={90}
                                                    fill="#8884d8"
                                                    dataKey="value"
                                                >
                                                    {prepareHashtagData().map((entry, index) => (
                                                        <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                                                    ))}
                                                </Pie>
                                                <Tooltip />
                                            </PieChart>
                                        </ResponsiveContainer>
                                    </div>
                                )}
                            </div>
                        )}

                        {/* AI Report */}
                        <div className="bg-white rounded-2xl shadow-xl p-8 border border-gray-100">
                            <div className="flex items-center justify-between mb-6">
                                <h3 className="text-2xl font-bold text-gray-900 flex items-center gap-2">
                                    🤖 Relatório Estratégico (IA)
                                </h3>
                                <button
                                    onClick={generatePDF}
                                    className="px-6 py-3 bg-gradient-to-r from-green-600 to-emerald-600 text-white font-semibold rounded-xl hover:from-green-700 hover:to-emerald-700 transition-all flex items-center space-x-2 shadow-lg"
                                >
                                    <Download className="h-4 w-4" />
                                    <span>Exportar PDF</span>
                                </button>
                            </div>

                            <div className="space-y-6">
                                {analysis.relatorio_ia.resumo_negocio && (
                                    <div className="bg-gradient-to-r from-purple-50 to-pink-50 p-6 rounded-xl">
                                        <h4 className="text-lg font-semibold text-gray-800 mb-3 flex items-center gap-2">
                                            📋 Resumo do Negócio
                                        </h4>
                                        <p className="text-gray-700 leading-relaxed">{analysis.relatorio_ia.resumo_negocio}</p>
                                    </div>
                                )}

                                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                                    {analysis.relatorio_ia.pontos_fortes && (
                                        <div className="bg-green-50 p-6 rounded-xl border-2 border-green-200">
                                            <h4 className="text-lg font-semibold text-green-800 mb-3 flex items-center gap-2">
                                                ✅ Pontos Fortes
                                            </h4>
                                            <p className="text-gray-700 leading-relaxed">{analysis.relatorio_ia.pontos_fortes}</p>
                                        </div>
                                    )}

                                    {analysis.relatorio_ia.pontos_fracos && (
                                        <div className="bg-red-50 p-6 rounded-xl border-2 border-red-200">
                                            <h4 className="text-lg font-semibold text-red-800 mb-3 flex items-center gap-2">
                                                ⚠️ Pontos Fracos
                                            </h4>
                                            <p className="text-gray-700 leading-relaxed">{analysis.relatorio_ia.pontos_fracos}</p>
                                        </div>
                                    )}
                                </div>

                                {analysis.relatorio_ia.oportunidades && (
                                    <div className="bg-blue-50 p-6 rounded-xl border-2 border-blue-200">
                                        <h4 className="text-lg font-semibold text-blue-800 mb-3 flex items-center gap-2">
                                            💡 Oportunidades
                                        </h4>
                                        <p className="text-gray-700 leading-relaxed">{analysis.relatorio_ia.oportunidades}</p>
                                    </div>
                                )}

                                {analysis.relatorio_ia.sugestao_prospeccao && (
                                    <div className="bg-gradient-to-r from-purple-100 to-pink-100 p-6 rounded-xl border-2 border-purple-300">
                                        <h4 className="text-lg font-semibold text-purple-900 mb-3 flex items-center gap-2">
                                            🎯 Sugestão de Abordagem
                                        </h4>
                                        <p className="text-gray-800 leading-relaxed font-medium">{analysis.relatorio_ia.sugestao_prospeccao}</p>
                                    </div>
                                )}

                                {/* Fallback para quando não há campos estruturados */}
                                {!analysis.relatorio_ia.resumo_negocio && (
                                    <div className="bg-gray-50 p-6 rounded-xl">
                                        <pre className="whitespace-pre-wrap font-sans text-gray-700 text-sm">
                                            {JSON.stringify(analysis.relatorio_ia, null, 2)}
                                        </pre>
                                    </div>
                                )}
                            </div>
                        </div>
                    </div>
                )}
            </main>

            {/* Footer */}
            <footer className="bg-gradient-to-r from-purple-900 to-pink-900 text-white py-8 mt-16">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
                    <p className="text-gray-200 mb-2">
                        © 2025 Instagram Analyzer - Desenvolvido para análise estratégica de perfis
                    </p>
                    <p className="text-gray-400 text-sm">
                        Powered by IA • Dados em tempo real (quando disponível)
                    </p>
                </div>
            </footer>
        </div>
    )
}

function Hash(props: React.SVGProps<SVGSVGElement>) {
    return (
        <svg
            {...props}
            xmlns="http://www.w3.org/2000/svg"
            width="24"
            height="24"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
        >
            <line x1="4" y1="9" x2="20" y2="9"></line>
            <line x1="4" y1="15" x2="20" y2="15"></line>
            <line x1="10" y1="3" x2="8" y2="21"></line>
            <line x1="16" y1="3" x2="14" y2="21"></line>
        </svg>
    )
}