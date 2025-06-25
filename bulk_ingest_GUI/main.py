"""
Archivo principal de la aplicación Bulk Ingest GUI
Lanza la aplicación y conecta todos los componentes
"""

import sys
import os
from pathlib import Path

# Configurar sys.path para importaciones absolutas
current_dir = Path(__file__).parent.resolve()
project_root = current_dir.parent.resolve()
sys.path.insert(0, str(current_dir))
sys.path.insert(0, str(project_root))

# Importar constantes necesarias ANTES de setup_environment
from gui_utils.constants import APP_NAME, VERSION

def setup_environment():
    """Configura el entorno de la aplicación"""
    # Usar directorios del servidor MCP organizado
    mcp_server_dir = project_root / "mcp_server_organized"
    
    # Asegurar que los directorios del servidor MCP existan usando su función
    try:
        # Importar la configuración del servidor MCP
        from utils.config import Config
        
        # Asegurar que los directorios existan
        Config.ensure_directories()
        
        print(f"[bold green]✅ Directorios del servidor MCP verificados:[/bold green]")
        print(f"[bold green]  📁 Documents: {Config.CONVERTED_DOCS_DIR}[/bold green]")
        print(f"[bold green]  📁 Vector Store: {Config.VECTOR_STORE_DIR}[/bold green]")
        print(f"[bold green]  📁 Embedding Cache: {Config.EMBEDDING_CACHE_DIR}[/bold green]")
        
    except ImportError as e:
        print(f"[bold yellow]⚠️ No se pudo importar la configuración del servidor MCP: {e}[/bold yellow]")
        print(f"[bold yellow]  Creando directorios manualmente...[/bold yellow]")
        
        # Fallback: crear directorios manualmente
        server_directories = {
            "embedding_cache": mcp_server_dir / "embedding_cache",
            "vector_store": mcp_server_dir / "data" / "vector_store",
            "documents": mcp_server_dir / "data" / "documents"
        }
        
        for name, path in server_directories.items():
            path.mkdir(parents=True, exist_ok=True)
            print(f"[bold green]✅ Directorio {name}: {path}[/bold green]")
    
    print(f"[bold green]✅ Entorno configurado para {APP_NAME} v{VERSION}[/bold green]")
    print(f"[bold blue]📁 Usando directorios del servidor MCP: {mcp_server_dir}[/bold blue]")

# Configurar el entorno ANTES de importar cualquier módulo que use rag_core
setup_environment()

import tkinter as tk
from services.configuration_service import ConfigurationService
from controllers.main_controller import MainController
from views.main_view import MainView
from gui_utils.exceptions import BulkIngestError

# Importar Rich para mejorar la salida en consola
from rich import print
from rich.panel import Panel


def create_application():
    """Crea y configura la aplicación principal"""
    try:
        # Crear ventana principal
        root = tk.Tk()
        
        # Configurar la ventana
        root.title(f"{APP_NAME} v{VERSION}")
        root.geometry("1200x800")
        root.minsize(1000, 700)
        
        # Configurar icono si existe
        icon_path = current_dir / "assets" / "icon.ico"
        if icon_path.exists():
            try:
                root.iconbitmap(icon_path)
            except:
                pass  # Ignorar si no se puede cargar el icono
        
        # Crear servicios
        config_service = ConfigurationService()
        
        # Crear controlador
        controller = MainController(root, config_service)
        
        # Crear vista principal
        main_view = MainView(root, controller)
        
        # Configurar cierre de ventana
        def on_closing():
            try:
                controller.cleanup()
                root.destroy()
            except Exception as e:
                print(Panel(f"[bold red]Error durante el cierre: {e}[/bold red]", title="[red]Error[/red]"))
                root.destroy()
        
        root.protocol("WM_DELETE_WINDOW", on_closing)
        
        return root, controller, main_view
        
    except Exception as e:
        print(Panel(f"[bold red]❌ Error creando la aplicación: {e}[/bold red]", title="[red]Error[/red]"))
        raise


def main():
    """Función principal que lanza la aplicación"""
    try:
        print(Panel(f"[bold blue]🚀 Iniciando {APP_NAME} v{VERSION}[/bold blue]", title="[cyan]Inicio[/cyan]"))
        print("[cyan]" + "=" * 50 + "[/cyan]")
        
        # Crear aplicación
        root, controller, main_view = create_application()
        
        print("[bold green]✅ Aplicación creada exitosamente[/bold green]")
        print("[bold magenta]📋 Funcionalidades disponibles:[/bold magenta]")
        print("[yellow]   • Procesamiento de documentos con rag_core.py[/yellow]")
        print("[yellow]   • Chunking semántico avanzado[/yellow]")
        print("[yellow]   • Cache de embeddings optimizado[/yellow]")
        print("[yellow]   • Almacenamiento en base vectorial[/yellow]")
        print("[yellow]   • Exportar/importar listas de documentos[/yellow]")
        print("[yellow]   • Filtros y búsqueda[/yellow]")
        print("[cyan]" + "=" * 50 + "[/cyan]")
        
        # Iniciar loop principal
        root.mainloop()
        
    except Exception as e:
        print(Panel(f"[bold red]💥 Error fatal en la aplicación: {e}[/bold red]", title="[red]Error Fatal[/red]"))
        print("[red]Detalles del error:[/red]")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main() 