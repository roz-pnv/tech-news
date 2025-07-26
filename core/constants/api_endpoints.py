API_ENDPOINTS = {
    "api_root": {
        "description": "Root endpoint for the API overview",
        "path": "/api/"
    },
    "news_list": {
        "description": "Get published news list",
        "path": "/news/"
    },
    "news_create": {
        "description": "Create a new news article",
        "path": "/news/create/"
    },
    "news_update": {
        "description": "Update a news article completely by slug",
        "path": "/news/<slug:slug>/update/"
    },
    "news_partial_update": {
        "description": "Partially update a news article by slug",
        "path": "/news/<slug:slug>/partial/"
    },
	"news_delete": {
        "description": "Delete a news article by slug",
        "path": "/news/<slug:slug>/delete/"
    },
    "auth_register": {
        "description": "Register a new user account",
        "path": "/auth/users/"
    },
    "auth_login": {
        "description": "Obtain JWT token",
        "path": "/auth/jwt/create/"
    },
    "auth_refresh": {
        "description": "Refresh JWT token",
        "path": "/auth/jwt/refresh/"
    },
    "auth_logout": {
        "description": "Logout and blacklist token",
        "path": "/auth/jwt/logout/"
    },
    "auth_me": {
        "description": "Get current user profile",
        "path": "/auth/users/me/"
    },
    "schema_raw": {
        "description": "Download raw OpenAPI schema",
        "path": "/api/schema/"
    },
    "schema_docs": {
        "description": "Interactive API documentation",
        "path": "/api/schema/docs/"
    }
}
