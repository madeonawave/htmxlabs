# HTMX Labs

HTMX Labs is the codebase for [htmxlabs.com](https://htmxlabs.com), a website dedicated to showcasing the possibilities of [htmx](https://htmx.org/). 
The site features a large collection of interactive examples and demos that illustrate how htmx can be used to build modern, dynamic web applications with minimal JavaScript.

The backend is built with Django, serving both the main site and all example endpoints. Each example demonstrates a specific htmx feature or integration, such as AJAX requests, real-time updates, form handling, UI components, and more. 
The project is designed to be a resource for learning and experimenting with htmx in a real-world context.

**Key Features:**
- Dozens of live, interactive htmx examples (AJAX, forms, tables, real-time, integrations, and more)
- Django backend serving all examples and fragments
- Modern frontend with Bulma CSS and custom styles
- Easy to extend with new examples

Visit [htmxlabs.com](https://htmxlabs.com) to see it in action!

## Author

- [madeonawave](https://github.com/madeonawave)

## Contributing

Contributions, issues and feature requests are welcome!

- Fork the repository
- Create your feature branch (`git checkout -b feature/your-feature`)
- Commit your changes (`git commit -am 'Add new feature'`)
- Push to the branch (`git push origin feature/your-feature`)
- Create a new Pull Request


## install
 - git clone the project
 - $ uv sync
 - create a file site/config/.env   
   * SECRET_KEY=secret-key-here 
   * DEBUG=True 
   * ALLOWED_HOST=*,htmxlabs.com,localhost
   * CSRF_TRUSTED_ORIGINS=http://localhost

## License

This project is licensed under the MIT License.

## Acknowledgements

- [HTMX](https://htmx.org/)
- [Django](https://www.djangoproject.com/)
- [Bulma](https://bulma.io/)
- [Leaflet](https://leafletjs.com/)
