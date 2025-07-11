import requests
import json
from datetime import datetime

def send_discord_notification(webhook_url, message, embed=None):
    """Envia notificação para o Discord"""
    if not webhook_url:
        return False
    
    data = {"content": message}
    
    # Se embed for fornecido, adiciona ao payload
    if embed:
        data["embeds"] = [embed]
    
    try:
        response = requests.post(webhook_url, json=data)
        return response.status_code == 204 or response.status_code == 200
    except Exception as e:
        print(f"Erro ao enviar notificação para o Discord: {e}")
        return False

def create_status_embed(title, description, color, fields=None):
    """Cria um embed para status do bot"""
    embed = {
        "title": title,
        "description": description,
        "color": color,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "footer": {
            "text": "KeyDrop Bot - Professional Edition",
            "icon_url": "https://cdn.discordapp.com/emojis/894678089630720010.png"
        }
    }
    
    if fields:
        embed["fields"] = fields
    
    return embed

def notify_bot_started(webhook_url, num_bots):
    """Notifica que o bot foi iniciado"""
    embed = create_status_embed(
        title="🚀 Bot KeyDrop Iniciado!",
        description=f"O bot foi iniciado com sucesso com {num_bots} janela(s).",
        color=3066993,  # Verde
        fields=[
            {
                "name": "📊 Status",
                "value": "✅ Online e funcionando",
                "inline": True
            },
            {
                "name": "🪟 Janelas",
                "value": f"{num_bots} perfis ativos",
                "inline": True
            },
            {
                "name": "⏰ Horário",
                "value": datetime.now().strftime("%d/%m/%Y às %H:%M:%S"),
                "inline": False
            }
        ]
    )
    
    return send_discord_notification(webhook_url, "", embed)

def notify_bot_stopped(webhook_url, reason="Manual"):
    """Notifica que o bot foi parado"""
    embed = create_status_embed(
        title="⏹️ Bot KeyDrop Parado",
        description="O bot foi encerrado.",
        color=15158332,  # Vermelho
        fields=[
            {
                "name": "📊 Status",
                "value": "❌ Offline",
                "inline": True
            },
            {
                "name": "🔄 Motivo",
                "value": reason,
                "inline": True
            },
            {
                "name": "⏰ Horário",
                "value": datetime.now().strftime("%d/%m/%Y às %H:%M:%S"),
                "inline": False
            }
        ]
    )
    
    return send_discord_notification(webhook_url, "", embed)

def notify_bot_error(webhook_url, error_message):
    """Notifica erro no bot"""
    embed = create_status_embed(
        title="⚠️ Erro no Bot KeyDrop",
        description=f"Um erro foi detectado: {error_message}",
        color=16776960,  # Amarelo
        fields=[
            {
                "name": "🚨 Tipo",
                "value": "Erro de funcionamento",
                "inline": True
            },
            {
                "name": "⏰ Horário",
                "value": datetime.now().strftime("%d/%m/%Y às %H:%M:%S"),
                "inline": True
            }
        ]
    )
    
    return send_discord_notification(webhook_url, "", embed)

def notify_automatic_report(webhook_url, embed_data):
    """Envia relatório automático para o Discord"""
    if not webhook_url:
        return False
    
    try:
        response = requests.post(webhook_url, json={"embeds": [embed_data]})
        return response.status_code == 204 or response.status_code == 200
    except Exception as e:
        print(f"Erro ao enviar relatório automático: {e}")
        return False

def create_report_embed(stats, period_hours):
    """Cria embed para relatório automático"""
    # Calcular métricas
    total_participacoes = stats['amateur_total'] + stats['contender_total']
    performance_hora = total_participacoes / period_hours if period_hours > 0 else 0
    
    # Status geral
    if stats['bots_ativos'] == stats['bots_total']:
        status_geral = "🟢 Todos os bots funcionando"
        cor = 3066993  # Verde
    elif stats['bots_ativos'] > stats['bots_total'] * 0.5:
        status_geral = f"🟡 {stats['bots_ativos']}/{stats['bots_total']} bots ativos"
        cor = 16776960  # Amarelo
    else:
        status_geral = f"🔴 {stats['bots_ativos']}/{stats['bots_total']} bots ativos"
        cor = 15548997  # Vermelho
    
    # Formatação do tempo
    if period_hours < 1:
        tempo_formatado = f"{int(period_hours * 60)}min"
    elif period_hours < 24:
        tempo_formatado = f"{period_hours:.1f}h"
    else:
        dias = int(period_hours // 24)
        horas_rest = period_hours % 24
        tempo_formatado = f"{dias}d {horas_rest:.1f}h"
    
    embed = {
        "title": "📊 RELATÓRIO AUTOMÁTICO - 12 HORAS",
        "description": f"Relatório do período de **{tempo_formatado}**",
        "color": cor,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "fields": [
            {
                "name": "🎯 **PARTICIPAÇÕES**",
                "value": f"```\n🏆 AMATEUR: {stats['amateur_total']:,}\n🏆 CONTENDER: {stats['contender_total']:,}\n📈 Total: {total_participacoes:,}\n⚡ Performance: {performance_hora:.1f}/hora```",
                "inline": True
            },
            {
                "name": "💰 **GANHOS**",
                "value": f"```\n💵 Período: R$ {stats['ganho_total']:.2f}\n🏦 Saldo atual: R$ {stats['saldo_total_atual']:.2f}\n📊 Média/bot: R$ {stats['saldo_total_atual']/max(stats['bots_total'],1):.2f}```",
                "inline": True
            },
            {
                "name": "⚠️ **ERROS**",
                "value": f"```\n❌ Total: {stats['erros_total']:,}\n📊 Taxa: {(stats['erros_total']/max(total_participacoes,1)*100):.1f}%\n🔧 Média/bot: {stats['erros_total']/max(stats['bots_total'],1):.1f}```",
                "inline": True
            },
            {
                "name": "🤖 **STATUS GERAL**",
                "value": f"```\n{status_geral}\n🔢 Total: {stats['bots_total']} bots\n⏱️ Uptime médio: {tempo_formatado}```",
                "inline": False
            }
        ],
        "footer": {
            "text": "KeyDrop Bot - Relatório Automático",
            "icon_url": "https://cdn.discordapp.com/emojis/894678089630720010.png"
        }
    }
    
    return embed

def create_enhanced_report_embed(stats, period_hours, system_info=None):
    """Cria embed aprimorado para relatório automático"""
    # Calcular métricas
    total_participacoes = stats.get('amateur_total', 0) + stats.get('contender_total', 0)
    performance_hora = total_participacoes / period_hours if period_hours > 0 else 0
    
    # Dados do sistema
    if system_info is None:
        system_info = {
            'cpu_usage': 0,
            'ram_usage': 0,
            'chrome_processes': 0,
            'network_usage': 0,
            'guias_reiniciadas': 0
        }
    
    # Status geral baseado em múltiplos fatores
    bots_ativos = stats.get('bots_ativos', 0)
    bots_total = stats.get('bots_total', 1)
    erro_rate = (stats.get('erros_total', 0) / max(total_participacoes, 1)) * 100
    
    if bots_ativos == bots_total and erro_rate < 10:
        status_geral = "🟢 Excelente performance"
        cor = 3066993  # Verde
    elif bots_ativos >= bots_total * 0.7 and erro_rate < 20:
        status_geral = f"🟡 Boa performance ({bots_ativos}/{bots_total})"
        cor = 16776960  # Amarelo
    else:
        status_geral = f"🔴 Performance reduzida ({bots_ativos}/{bots_total})"
        cor = 15548997  # Vermelho
    
    # Formatação do tempo
    if period_hours < 1:
        tempo_formatado = f"{int(period_hours * 60)}min"
    elif period_hours < 24:
        tempo_formatado = f"{period_hours:.1f}h"
    else:
        dias = int(period_hours // 24)
        horas_rest = period_hours % 24
        tempo_formatado = f"{dias}d {horas_rest:.1f}h"
    
    # Calcular lucro médio por hora
    lucro_hora = stats.get('ganho_total', 0) / period_hours if period_hours > 0 else 0
    
    embed = {
        "title": f"📊 RELATÓRIO AUTOMÁTICO - {tempo_formatado.upper()}",
        "description": f"**Período:** {tempo_formatado} | **IP:** {get_public_ip()}",
        "color": cor,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "fields": [
            {
                "name": "🎯 **PARTICIPAÇÕES**",
                "value": f"```\n🥉 Amateur: {stats.get('amateur_total', 0):,}\n🏆 Contender: {stats.get('contender_total', 0):,}\n📈 Total: {total_participacoes:,}\n⚡ Performance: {performance_hora:.1f}/h```",
                "inline": True
            },
            {
                "name": "💰 **FINANCEIRO**",
                "value": f"```\n💵 Lucro período: R$ {stats.get('ganho_total', 0):.2f}\n💳 Saldo atual: R$ {stats.get('saldo_total_atual', 0):.2f}\n📊 Lucro/hora: R$ {lucro_hora:.2f}\n💎 Skins: {stats.get('total_skins', 0)}```",
                "inline": True
            },
            {
                "name": "⚠️ **ERROS E PROBLEMAS**",
                "value": f"```\n❌ Total erros: {stats.get('erros_total', 0):,}\n📊 Taxa erro: {erro_rate:.1f}%\n🔄 Guias reiniciadas: {system_info.get('guias_reiniciadas', 0)}\n🛠️ Avg/bot: {stats.get('erros_total', 0)/max(bots_total,1):.1f}```",
                "inline": True
            },
            {
                "name": "🖥️ **SISTEMA**",
                "value": f"```\n💻 CPU: {system_info.get('cpu_usage', 0):.1f}%\n🧠 RAM: {system_info.get('ram_usage', 0):.1f}%\n🌐 Chrome: {system_info.get('chrome_processes', 0)} proc.\n📶 Rede: {system_info.get('network_usage', 0):.1f} MB```",
                "inline": True
            },
            {
                "name": "🤖 **BOTS**",
                "value": f"```\n{status_geral}\n🔢 Ativos: {bots_ativos}/{bots_total}\n⏱️ Uptime: {tempo_formatado}\n🔥 Bots simultâneos: {bots_total}```",
                "inline": True
            },
            {
                "name": "📊 **CONSUMO**",
                "value": f"```\n🌐 Internet: {system_info.get('network_usage', 0)/1024:.2f} GB\n💾 Disco: {system_info.get('disk_usage', 0):.1f}%\n🔋 Eficiência: {(total_participacoes/max(stats.get('erros_total',1),1)):.1f}x\n⭐ Score: {min(100, max(0, 100-erro_rate)):.0f}/100```",
                "inline": True
            }
        ],
        "footer": {
            "text": "KeyDrop Bot Professional - Relatório Automático",
            "icon_url": "https://cdn.discordapp.com/emojis/894678089630720010.png"
        }
    }
    
    return embed

def get_public_ip():
    """Obtém IP público"""
    try:
        import requests
        response = requests.get('https://httpbin.org/ip', timeout=5)
        return response.json().get('origin', 'IP não disponível')
    except:
        try:
            response = requests.get('https://ipinfo.io/ip', timeout=5)
            return response.text.strip()
        except:
            return 'IP não disponível'

def get_system_info():
    """Coleta informações do sistema"""
    try:
        import psutil
        
        # CPU e RAM
        cpu_percent = psutil.cpu_percent(interval=1)
        ram = psutil.virtual_memory()
        ram_percent = ram.percent
        
        # Processos Chrome
        chrome_count = 0
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                if 'chrome' in proc.info['name'].lower():
                    chrome_count += 1
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        
        # Uso de rede (aproximado)
        net_io = psutil.net_io_counters()
        network_usage = (net_io.bytes_sent + net_io.bytes_recv) / (1024 * 1024)  # MB
        
        # Uso de disco
        disk_usage = psutil.disk_usage('/').percent
        
        return {
            'cpu_usage': cpu_percent,
            'ram_usage': ram_percent,
            'chrome_processes': chrome_count,
            'network_usage': network_usage,
            'disk_usage': disk_usage,
            'guias_reiniciadas': 0  # Será preenchido pelo bot
        }
    except:
        return {
            'cpu_usage': 0,
            'ram_usage': 0,
            'chrome_processes': 0,
            'network_usage': 0,
            'disk_usage': 0,
            'guias_reiniciadas': 0
        }

def send_enhanced_report(webhook_url, stats, period_hours=12, system_info=None):
    """Envia relatório aprimorado para o Discord"""
    if not webhook_url:
        return False
    
    if system_info is None:
        system_info = get_system_info()
    
    embed = create_enhanced_report_embed(stats, period_hours, system_info)
    
    try:
        response = requests.post(webhook_url, json={"embeds": [embed]})
        return response.status_code == 204 or response.status_code == 200
    except Exception as e:
        print(f"Erro ao enviar relatório aprimorado: {e}")
        return False
