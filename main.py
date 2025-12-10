
"""
Sistema de Gestión de Gimnasio - GymForTheMoment
Aplicación desarrollada con patrón MVC (Modelo-Vista-Controlador)
"""

import sys
import os

# Add the project root to sys.path at the very beginning
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Now import the app
from views.app import GymApp

def main():
    """Función principal para iniciar la aplicación"""
    try:
        app = GymApp()
        app.mainloop()
    except KeyboardInterrupt:
        print("\n✋ Aplicación cerrada por el usuario")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Error al iniciar la aplicación: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()