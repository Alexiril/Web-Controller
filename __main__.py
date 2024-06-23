if __name__ == "__main__":
    # Load confuguration
    from core.Config import *
    # Build routes
    from core.Router import *
    
    from core.Server import Server
    Server().run()
