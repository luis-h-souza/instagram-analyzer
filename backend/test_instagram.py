"""
Script de diagnóstico para testar conexão com Instagram
Ajuda a identificar o problema específico
"""

import instaloader
import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

def test_instagram_connection():
    print("="*60)
    print("🔍 DIAGNÓSTICO DE CONEXÃO COM INSTAGRAM")
    print("="*60)
    
    username = os.getenv("INSTAGRAM_USERNAME")
    password = os.getenv("INSTAGRAM_PASSWORD")
    
    if not username or not password:
        print("❌ Erro: Credenciais não encontradas no .env")
        return
    
    print(f"\n✅ Credenciais encontradas")
    print(f"   Username: {username}")
    print(f"   Password: {'*' * len(password)}")
    
    # Criar Instaloader
    L = instaloader.Instaloader(
        download_pictures=False,
        download_videos=False,
        download_comments=False,
        save_metadata=False,
        quiet=False
    )
    
    # Testar login
    print("\n🔐 Testando login...")
    try:
        session_file = Path(f"session-{username}")
        
        if session_file.exists():
            print(f"   📦 Sessão encontrada: {session_file}")
            try:
                L.load_session_from_file(username, str(session_file))
                print("   ✅ Sessão carregada com sucesso")
            except Exception as e:
                print(f"   ⚠️ Erro ao carregar sessão: {e}")
                print("   🔄 Fazendo novo login...")
                L.login(username, password)
                L.save_session_to_file(str(session_file))
                print("   ✅ Novo login realizado")
        else:
            print("   📝 Primeira vez - fazendo login...")
            L.login(username, password)
            L.save_session_to_file(str(session_file))
            print("   ✅ Login realizado e sessão salva")
    
    except Exception as e:
        print(f"   ❌ Erro no login: {e}")
        return
    
    # Testar perfil simples
    print("\n👤 Testando acesso a perfil (instagram)...")
    try:
        profile = instaloader.Profile.from_username(L.context, "instagram")
        print(f"   ✅ Perfil acessado com sucesso")
        print(f"   📊 Seguidores: {profile.followers:,}")
        print(f"   📊 Posts: {profile.mediacount:,}")
    except Exception as e:
        print(f"   ❌ Erro ao acessar perfil: {e}")
        return
    
    # Testar coleta de posts
    print("\n📸 Testando coleta de posts...")
    try:
        posts_count = 0
        max_posts = 3
        
        for post in profile.get_posts():
            if posts_count >= max_posts:
                break
            
            print(f"   ✅ Post {posts_count + 1}:")
            print(f"      Likes: {post.likes:,}")
            print(f"      Comments: {post.comments:,}")
            print(f"      Date: {post.date_local}")
            
            posts_count += 1
        
        if posts_count > 0:
            print(f"\n   ✅ Conseguiu coletar {posts_count} posts!")
        else:
            print(f"\n   ⚠️ Não conseguiu coletar nenhum post")
    
    except Exception as e:
        error_msg = str(e).lower()
        print(f"   ❌ Erro ao coletar posts: {e}")
        
        if "401" in str(e) or "wait" in error_msg:
            print("\n   🔴 DIAGNÓSTICO: Rate Limiting Detectado")
            print("   📋 Recomendações:")
            print("      1. Aguarde 5-30 minutos antes de tentar novamente")
            print("      2. Use dados mock enquanto aguarda")
            print("      3. Considere usar proxy ou mudar de IP")
            print("      4. Verifique se há muitas requisições recentes")
        
        elif "login" in error_msg or "authentication" in error_msg:
            print("\n   🔐 DIAGNÓSTICO: Problema de Autenticação")
            print("   📋 Recomendações:")
            print("      1. Verifique se username e password estão corretos")
            print("      2. Tente fazer login manual no navegador")
            print("      3. Desative 2FA temporariamente")
            print("      4. Delete session-* e tente novamente")
        
        elif "private" in error_msg:
            print("\n   🔒 DIAGNÓSTICO: Perfil Privado")
            print("   📋 Recomendações:")
            print("      1. Siga o perfil com sua conta")
            print("      2. Use dados mock para demonstração")
        
        else:
            print("\n   ❓ DIAGNÓSTICO: Erro Desconhecido")
            print("   📋 Recomendações:")
            print("      1. Verifique sua conexão com internet")
            print("      2. Tente usar VPN")
            print("      3. Aguarde alguns minutos")
            print("      4. Use modo mock")
        
        return
    
    # Resumo final
    print("\n" + "="*60)
    print("📊 RESUMO DO DIAGNÓSTICO")
    print("="*60)
    print("✅ Login: OK")
    print("✅ Acesso ao perfil: OK")
    print(f"{'✅' if posts_count > 0 else '⚠️'} Coleta de posts: {'OK' if posts_count > 0 else 'BLOQUEADO'}")
    
    if posts_count > 0:
        print("\n🎉 Tudo funcionando! Sua aplicação deve funcionar normalmente.")
    else:
        print("\n⚠️ ATENÇÃO: Instagram está bloqueando coleta de posts!")
        print("   Sua aplicação funcionará parcialmente:")
        print("   ✅ Dados básicos do perfil (nome, bio, seguidores)")
        print("   ❌ Métricas de engajamento (precisa de posts)")
        print("\n   💡 Use o endpoint /analisar-mock/{username} enquanto aguarda")
    
    print("="*60)

if __name__ == "__main__":
    test_instagram_connection()