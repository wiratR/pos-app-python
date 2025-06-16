from views.home_view import HomeView

def load_view(view_name: str):
    if view_name == "home":
        return HomeView()
    else:
        raise ValueError(f"Unknown view: {view_name}")