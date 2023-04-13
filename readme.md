# Building a ChatGPT Plugin: AI Web Surfer
<div align="right">
<img src="https://raw.githubusercontent.com/ruvnet/Surfer/main/assets/screen-shot.png">
</div>

### Built using my ChatGPT Plugin Bot.
Plugin Creator Bot. https://github.com/ruvnet/Bot-Generator-Bot/blob/main/prompts/chatgpt-plugin-generator.txt

### Code
https://github.com/ruvnet/Surfer/blob/main/main.py

## Introduction
ChatGPT plugins are a powerful way to extend the capabilities of the ChatGPT language model by integrating external APIs and services. In this blog post, we'll explore how to build a ChatGPT plugin called "AI Surfer" that allows ChatGPT to surf the internet, summarize articles, and limit token counts using concurrent API connections. We'll also discuss how to deploy the plugin to Replit for free or to other cloud services.

## What are ChatGPT Plugins?
ChatGPT plugins are integrations that allow ChatGPT to interact with external APIs, databases, or services. By using plugins, ChatGPT can perform tasks such as fetching data, summarizing articles, translating text, and much more. Plugins are defined using a manifest file (ai-plugin.json) and an OpenAPI specification (specification.yaml) that describe the plugin's metadata, authentication, and API endpoints.

## AI Surfer Plugin: Overview
The AI Surfer plugin empowers ChatGPT to "surf" the internet by summarizing the content of web pages provided by users. By inputting a URL, the plugin leverages OpenAI's GPT-3.5 Turbo language model to generate concise and informative summaries of the web page's content. The plugin's key features and benefits include:

- **Web Content Summarization**: The AI Surfer plugin can distill the essential information from articles, blog posts, and other web content, providing users with quick and easy-to-understand summaries.

- **Concurrent API Connections**: To efficiently handle long articles and reduce token counts, the plugin uses concurrent API connections to process and summarize different sections of the content simultaneously.

- **Language Model Integration**: The plugin integrates with OpenAI's GPT-3.5 Turbo language model, harnessing its natural language processing capabilities to produce high-quality summaries.

- **Adjustability and Flexibility**: The plugin is fully adjustable, allowing developers to customize its behavior and output to suit specific use cases.

- **Deployment Options**: The AI Surfer plugin can be deployed to various cloud services, including Replit, AWS, Heroku, and more, providing flexibility in hosting and scalability.

By enabling ChatGPT to summarize web content, the AI Surfer plugin enhances the language model's capabilities, allowing users to quickly access and understand information from across the web.

## Introduction to OpenAI Plugin Creation and Specifications

OpenAI's ChatGPT plugins provide a powerful way to extend the capabilities of the ChatGPT language model by integrating it with external APIs and services. By creating plugins, developers can enable ChatGPT to perform a wide range of tasks, such as fetching data from external sources, summarizing articles, translating text, and much more.

To create a ChatGPT plugin, developers need to provide a plugin manifest file that includes metadata about the plugin, authentication details, and an API specification. The manifest file is a JSON file that follows a specific schema defined by OpenAI. The API specification is typically provided in the OpenAPI (Swagger) format, which describes the endpoints and operations that the plugin can perform.

### Plugin Manifest

The plugin manifest is a JSON file named `ai-plugin.json` that must be hosted in a publicly accessible location on the developer's server under the `.well-known` directory (e.g., `https://example.com/.well-known/ai-plugin.json`). The manifest file contains the following key fields:

- `schema_version`: The manifest schema version (e.g., `"v1"`).
- `name_for_human`: A human-readable name for the plugin, such as the full company name.
- `name_for_model`: A name that the ChatGPT model will use to target the plugin.
- `description_for_human`: A human-readable description of the plugin.
- `description_for_model`: A description tailored to the model, such as token context length considerations.
- `auth`: An object describing the authentication schema for the plugin (e.g., `"none"`, `"user_http"`, `"service_http"`, `"oauth"`).
- `api`: An object describing the API specification, including the type (e.g., `"openapi"`) and the URL to the OpenAPI specification file.
- `logo_url`: A URL used to fetch the plugin's logo (optional).
- `contact_email`: An email contact for safety/moderation reachout, support, and deactivation (optional).
- `legal_info_url`: A URL for users to view plugin information (optional).

### API Specification

The API specification is a YAML or JSON file that follows the OpenAPI (Swagger) format. It describes the available endpoints, operations, parameters, and responses that the plugin can perform. The API specification file must also be hosted on the developer's server and referenced in the plugin manifest's `api` field.

The OpenAPI specification serves as a wrapper that sits on top of the developer's API, allowing ChatGPT to understand and interact with the API. Developers can choose which endpoints and operations to expose to ChatGPT, providing control over the plugin's functionality.

### Hosting the Plugin

To deploy a ChatGPT plugin, developers need to host both the `ai-plugin.json` manifest file and the OpenAPI specification file on their server. These files must be publicly accessible and placed in the appropriate directories (e.g., `.well-known` for the manifest file). Developers can use various hosting services, such as AWS, Heroku, Replit, or their own servers, to host the plugin files.

Once the plugin is deployed and the files are hosted, developers can submit the plugin to OpenAI for review and approval. Once approved, the plugin becomes available for use by ChatGPT and its users.

By following the specifications and hosting requirements, developers can create and deploy powerful plugins that enhance the capabilities of ChatGPT and provide users with new and exciting functionalities.


## Building the AI Surfer Plugin
### Structure
```
/main.py                  # The main Python script that runs the FastAPI application and defines the endpoints
/plugins/ai-plugin.json   # The ChatGPT plugin manifest file containing metadata and API specification details
/plugins/logo.jpg         # The logo image file for the plugin, referenced in the manifest file
/plugins/openapi.yaml     # The OpenAPI (Swagger) specification file describing the plugin's API endpoints
/templates/index.html     # The HTML template for the main page where users can input a URL for summarization
/templates/summary.html   # The HTML template for displaying the summarized content to the user
/readme.md                # The README file containing documentation and instructions for using the plugin
/requirements.txt         # The file listing the Python dependencies required to run the application
```
### Step 1: Setting Up the Environment
To build the AI Surfer plugin, we'll use Python and the FastAPI framework. We'll also use libraries such as openai, requests, bs4 (BeautifulSoup), spacy, and httpx. Make sure to install these libraries and set up your environment.

### Step 2: Defining the FastAPI Application
We'll create a FastAPI application with endpoints for summarizing URLs and displaying summaries. The application will use the GPT-3.5 Turbo model to generate summaries in bullet points.

### Step 3: Implementing the Summarization Logic
The summarization logic involves fetching the HTML content of a URL, extracting the text content, and using the GPT-3.5 Turbo model to generate summaries. We'll use concurrent API connections to process article chunks simultaneously and limit token counts.

### Step 4: Creating the Plugin Manifest (ai-plugin.json)
The plugin manifest file describes the plugin's metadata, authentication, and API specification. The manifest includes fields such as name_for_human, description_for_model, auth, and api. The auth field specifies the authentication type (e.g., "none" for no authentication).

### Step 5: Creating the OpenAPI Specification (specification.yaml)
The OpenAPI specification documents the API endpoints of the plugin. It defines the paths, parameters, and responses for each endpoint. ChatGPT uses this specification to understand how to interact with the plugin's API.

### Step 6: Deploying the Plugin
The AI Surfer plugin can be deployed to Replit for free or to other cloud services. Make sure to set up environment variables (e.g., OpenAI API key) and configure the domain name in the manifest file.

## Buidl
Building a ChatGPT plugin is a great way to extend the capabilities of ChatGPT and provide users with new and exciting functionalities. The AI Surfer plugin is just one example of how plugins can be used to enhance the ChatGPT experience. Whether you're a beginner or an experienced developer, building ChatGPT plugins is a rewarding and creative endeavor.

For more information on ChatGPT plugins, including authentication options, manifest fields, and OpenAPI specifications, please refer to the official ChatGPT plugin documentation. 

Or try my Plugin Creator Bot. 
https://github.com/ruvnet/Bot-Generator-Bot/blob/main/prompts/chatgpt-plugin-generator.txt

*Note: This blog post is a high-level overview of building a ChatGPT plugin. For detailed code implementation, please refer to the AI Surfer plugin code provided earlier in this conversation.*

## Deploying the AI Surfer Plugin

To deploy the AI Surfer plugin, you can use Replit or any other cloud service of your choice. Here are the steps to deploy the plugin on Replit:

1. Create a new Replit project and upload the AI Surfer plugin code.
2. Set up environment variables in Replit, including the OpenAI API key (`OPENAI_API_KEY`) and the domain name (`DOMAIN_NAME`).
3. Update the `domain_name` variable in the code to use the Replit secret: `domain_name = os.getenv("DOMAIN_NAME")`.
4. Run the FastAPI application on Replit.

Once deployed, you can access the AI Surfer plugin using the provided URL and start summarizing articles.

In this blog post, we explored how to build a ChatGPT plugin called AI Surfer that allows ChatGPT to surf the internet and summarize articles. We discussed the implementation details, including fetching HTML content, extracting text, generating summaries using GPT-3.5 Turbo, and deploying the plugin to Replit.

Building ChatGPT plugins is an exciting way to extend the capabilities of ChatGPT and provide users with new functionalities. Whether you're summarizing articles, translating text, or fetching

# Appendix
## FastAPI 

FastAPI is a modern, fast (high-performance) web framework for building APIs with Python. It is designed to be easy to use, while also providing high performance and robustness. FastAPI is built on top of Starlette for web routing and Pydantic for data validation and serialization. It offers a wide range of features, including automatic generation of OpenAPI and JSON Schema documentation, dependency injection, OAuth2 and JWT authentication, and more.

In the AI Web Surfer plugin, FastAPI is used to create the web application and API endpoints that interact with OpenAI's GPT-3.5 Turbo language model. The plugin leverages FastAPI's asynchronous capabilities to efficiently handle concurrent requests and summarize long articles. FastAPI's automatic generation of OpenAPI documentation is also utilized to expose the API specification for the plugin, making it compatible with ChatGPT's plugin system.

One of the key benefits of using FastAPI is its comprehensive and well-organized documentation. The official FastAPI documentation provides detailed explanations, code examples, and best practices for building web applications and APIs. Whether you are a beginner or an experienced developer, the documentation is a valuable resource for learning how to use FastAPI effectively.

To explore the FastAPI documentation and learn more about its features, you can visit the official website: https://fastapi.tiangolo.com/

In summary, FastAPI is a powerful and versatile web framework that plays a crucial role in building the AI Web Surfer plugin. By using FastAPI, developers can create high-performance web applications and APIs that seamlessly integrate with ChatGPT and other AI language models.
