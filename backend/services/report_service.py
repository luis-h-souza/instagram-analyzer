from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
import os
from datetime import datetime
from typing import Dict, Any
import requests
from io import BytesIO

class ReportService:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._criar_estilos_personalizados()
    
    def _criar_estilos_personalizados(self):
        """Cria estilos personalizados para o relatório"""
        # Título principal
        self.styles.add(ParagraphStyle(
            name='TituloPrincipal',
            parent=self.styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#1DA1F2')
        ))
        
        # Subtítulo
        self.styles.add(ParagraphStyle(
            name='Subtitulo',
            parent=self.styles['Heading2'],
            fontSize=16,
            spaceAfter=20,
            textColor=colors.HexColor('#333333')
        ))
        
        # Texto normal
        self.styles.add(ParagraphStyle(
            name='TextoNormal',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=12,
            alignment=TA_LEFT
        ))
        
        # Destaque
        self.styles.add(ParagraphStyle(
            name='Destaque',
            parent=self.styles['Normal'],
            fontSize=12,
            spaceAfter=12,
            textColor=colors.HexColor('#1DA1F2'),
            fontName='Helvetica-Bold'
        ))
    
    def gerar_pdf(self, username: str, dados_perfil: Dict[str, Any], 
                  metricas: Dict[str, Any], relatorio_ia: Dict[str, str]) -> str:
        """
        Gera um relatório PDF completo
        """
        # Criar diretório se não existir
        os.makedirs("reports", exist_ok=True)
        
        # Nome do arquivo
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"relatorio_{username}_{timestamp}.pdf"
        filepath = os.path.join("reports", filename)
        
        # Criar documento PDF
        doc = SimpleDocTemplate(filepath, pagesize=A4, 
                               rightMargin=72, leftMargin=72,
                               topMargin=72, bottomMargin=18)
        
        # Elementos do relatório
        story = []
        
        # Cabeçalho
        story.append(Paragraph("📊 RELATÓRIO DE ANÁLISE INSTAGRAM", self.styles['TituloPrincipal']))
        story.append(Paragraph(f"Perfil: @{username}", self.styles['Subtitulo']))
        story.append(Paragraph(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}", self.styles['TextoNormal']))
        story.append(Spacer(1, 20))
        
        # Seção 1: Dados Básicos
        story.append(Paragraph("📋 DADOS BÁSICOS DO PERFIL", self.styles['Subtitulo']))
        
        dados_basicos = [
            ['Nome Completo', dados_perfil.get('nome_completo', 'N/A')],
            ['Biografia', dados_perfil.get('biografia', 'N/A')[:100] + '...' if len(dados_perfil.get('biografia', '')) > 100 else dados_perfil.get('biografia', 'N/A')],
            ['Seguidores', f"{dados_perfil.get('seguidores', 0):,}"],
            ['Seguindo', f"{dados_perfil.get('seguindo', 0):,}"],
            ['Total de Posts', f"{dados_perfil.get('total_posts', 0):,}"],
            ['Verificado', 'Sim' if dados_perfil.get('verificado', False) else 'Não'],
            ['Conta Privada', 'Sim' if dados_perfil.get('conta_privada', False) else 'Não']
        ]
        
        tabela_dados = Table(dados_basicos, colWidths=[2*inch, 4*inch])
        tabela_dados.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#F0F8FF')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('BACKGROUND', (1, 0), (1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(tabela_dados)
        story.append(Spacer(1, 20))
        
        # Seção 2: Métricas de Engajamento
        story.append(Paragraph("📈 MÉTRICAS DE ENGAJAMENTO", self.styles['Subtitulo']))
        
        metricas_dados = [
            ['Engajamento Médio', metricas.get('engajamento_medio', 'N/A')],
            ['Posts por Semana', str(metricas.get('posts_semanais', 0))],
            ['Média de Curtidas', f"{metricas.get('media_curtidas', 0):,}"],
            ['Média de Comentários', f"{metricas.get('media_comentarios', 0):,}"],
            ['Principais Hashtags', ', '.join(metricas.get('principais_hashtags', [])[:5])]
        ]
        
        tabela_metricas = Table(metricas_dados, colWidths=[2*inch, 4*inch])
        tabela_metricas.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#E8F5E8')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('BACKGROUND', (1, 0), (1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(tabela_metricas)
        story.append(Spacer(1, 20))
        
        # Seção 3: Análise de IA
        story.append(Paragraph("🤖 ANÁLISE ESTRATÉGICA (IA)", self.styles['Subtitulo']))
        
        # Resumo do Negócio
        story.append(Paragraph("Resumo do Negócio:", self.styles['Destaque']))
        story.append(Paragraph(relatorio_ia.get('resumo_negocio', 'N/A'), self.styles['TextoNormal']))
        story.append(Spacer(1, 12))
        
        # Pontos Fortes
        story.append(Paragraph("Pontos Fortes:", self.styles['Destaque']))
        story.append(Paragraph(relatorio_ia.get('pontos_fortes', 'N/A'), self.styles['TextoNormal']))
        story.append(Spacer(1, 12))
        
        # Pontos Fracos
        story.append(Paragraph("Pontos Fracos:", self.styles['Destaque']))
        story.append(Paragraph(relatorio_ia.get('pontos_fracos', 'N/A'), self.styles['TextoNormal']))
        story.append(Spacer(1, 12))
        
        # Oportunidades
        story.append(Paragraph("Oportunidades:", self.styles['Destaque']))
        story.append(Paragraph(relatorio_ia.get('oportunidades', 'N/A'), self.styles['TextoNormal']))
        story.append(Spacer(1, 12))
        
        # Sugestão de Prospecção
        story.append(Paragraph("Sugestão de Abordagem:", self.styles['Destaque']))
        story.append(Paragraph(relatorio_ia.get('sugestao_prospeccao', 'N/A'), self.styles['TextoNormal']))
        story.append(Spacer(1, 20))
        
        # Seção 4: Últimos Posts
        story.append(Paragraph("📱 ÚLTIMOS POSTS ANALISADOS", self.styles['Subtitulo']))
        
        posts = dados_perfil.get('posts', [])
        if posts:
            for i, post in enumerate(posts[:3], 1):
                story.append(Paragraph(f"Post {i}:", self.styles['Destaque']))
                
                post_info = [
                    ['Legenda', post.get('legenda', 'N/A')[:200] + '...' if len(post.get('legenda', '')) > 200 else post.get('legenda', 'N/A')],
                    ['Curtidas', f"{post.get('curtidas', 0):,}"],
                    ['Comentários', f"{post.get('comentarios', 0):,}"],
                    ['Tipo', post.get('tipo', 'N/A')],
                    ['Data', post.get('data_postagem', 'N/A')[:10]]
                ]
                
                tabela_post = Table(post_info, colWidths=[1.5*inch, 4.5*inch])
                tabela_post.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#FFF8DC')),
                    ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, -1), 9),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                    ('BACKGROUND', (1, 0), (1, -1), colors.white),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black)
                ]))
                
                story.append(tabela_post)
                story.append(Spacer(1, 15))
        else:
            story.append(Paragraph("Nenhum post encontrado para análise.", self.styles['TextoNormal']))
        
        # Rodapé
        story.append(Spacer(1, 30))
        story.append(Paragraph("Relatório gerado automaticamente pelo Instagram Analyzer", 
                              self.styles['TextoNormal']))
        
        # Construir PDF
        doc.build(story)
        
        return filepath
