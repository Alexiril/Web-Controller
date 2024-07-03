if __name__ == "__main__":
    # Build routes
    from core.Router import initialize as rinit
    rinit()
    # Load users
    from core.User import initialize as uinit
    uinit()
    # Load applications
    from core.Application import initialize as ainit
    ainit()
    
    from core.Server import Server
    Server().run()
