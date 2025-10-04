export const installConfigs = {
  cursor: {
    name: 'Cursor',
    description: 'Install brain-trust in Cursor IDE with HTTP transport.',
    installButton: 'https://cursor.com/en/install-mcp?name=brain-trust&config=eyJ1cmwiOiAiaHR0cDovL2xvY2FsaG9zdDo4MDAwL21jcCIsICJ0cmFuc3BvcnQiOiAiaHR0cCIsICJlbnYiOiB7Ik9QRU5BSV9BUElfS0VZIjogInlvdXJfb3BlbmFpX2FwaV9rZXlfaGVyZSJ9fQ==',
    steps: [
      {
        title: 'Start the server',
        description: 'Make sure Docker is running and start the brain-trust server:',
        code: 'docker-compose up -d',
      },
      {
        title: 'Manual Configuration',
        description: 'Or configure manually by adding to ~/.cursor/mcp.json:',
        code: `{
  "mcpServers": {
    "brain-trust": {
      "url": "http://localhost:8000/mcp",
      "transport": "http",
      "env": {
        "OPENAI_API_KEY": "your_openai_api_key_here"
      }
    }
  }
}`,
      },
      {
        title: 'Restart Cursor',
        description: 'Restart Cursor to load the new MCP server configuration.',
      },
    ],
    verification: 'Try asking: "Use phone_a_friend to ask: What is FastMCP?"',
  },

  claude_desktop: {
    name: 'Claude Desktop',
    description: 'Install brain-trust in Claude Desktop with HTTP transport.',
    steps: [
      {
        title: 'Start the server',
        description: 'Make sure Docker is running and start the brain-trust server:',
        code: 'docker-compose up -d',
      },
      {
        title: 'Configure Claude Desktop',
        description: 'Add to ~/Library/Application Support/Claude/claude_desktop_config.json (Mac) or %APPDATA%/Claude/claude_desktop_config.json (Windows):',
        code: `{
  "mcpServers": {
    "brain-trust": {
      "url": "http://localhost:8000/mcp",
      "transport": "http",
      "env": {
        "OPENAI_API_KEY": "your_openai_api_key_here"
      }
    }
  }
}`,
      },
      {
        title: 'Restart Claude Desktop',
        description: 'Restart Claude Desktop to load the MCP server.',
      },
    ],
    verification: 'The brain-trust tools should appear in the Claude Desktop interface.',
  },

  vscode: {
    name: 'VS Code',
    description: 'Install brain-trust in VS Code using the MCP extension.',
    steps: [
      {
        title: 'Install MCP Extension',
        description: 'Install the Model Context Protocol extension from the VS Code marketplace.',
      },
      {
        title: 'Start the server',
        description: 'Make sure Docker is running and start the brain-trust server:',
        code: 'docker-compose up -d',
      },
      {
        title: 'Configure MCP Extension',
        description: 'Add to .vscode/mcp.json in your workspace:',
        code: `{
  "mcpServers": {
    "brain-trust": {
      "url": "http://localhost:8000/mcp",
      "transport": "http",
      "env": {
        "OPENAI_API_KEY": "your_openai_api_key_here"
      }
    }
  }
}`,
      },
    ],
    verification: 'Check the MCP extension panel to see if brain-trust is connected.',
  },

  cline: {
    name: 'Cline',
    description: 'Install brain-trust in Cline with HTTP transport.',
    steps: [
      {
        title: 'Start the server',
        description: 'Make sure Docker is running and start the brain-trust server:',
        code: 'docker-compose up -d',
      },
      {
        title: 'Configure Cline',
        description: 'Add to Cline MCP settings:',
        code: `{
  "mcpServers": {
    "brain-trust": {
      "url": "http://localhost:8000/mcp",
      "transport": "http",
      "env": {
        "OPENAI_API_KEY": "your_openai_api_key_here"
      }
    }
  }
}`,
      },
    ],
    verification: 'The brain-trust tools should be available in Cline.',
  },

  windsurf: {
    name: 'Windsurf',
    description: 'Install brain-trust in Windsurf IDE with HTTP transport.',
    steps: [
      {
        title: 'Start the server',
        description: 'Make sure Docker is running and start the brain-trust server:',
        code: 'docker-compose up -d',
      },
      {
        title: 'Configure Windsurf',
        description: 'Add to Windsurf MCP configuration:',
        code: `{
  "mcpServers": {
    "brain-trust": {
      "url": "http://localhost:8000/mcp",
      "transport": "http",
      "env": {
        "OPENAI_API_KEY": "your_openai_api_key_here"
      }
    }
  }
}`,
      },
    ],
    verification: 'Check Windsurf MCP panel for brain-trust connection.',
  },

  roo_code: {
    name: 'Roo Code',
    description: 'Install brain-trust in Roo Code with HTTP transport.',
    steps: [
      {
        title: 'Start the server',
        description: 'Make sure Docker is running and start the brain-trust server:',
        code: 'docker-compose up -d',
      },
      {
        title: 'Configure Roo Code',
        description: 'Add to Roo Code MCP settings:',
        code: `{
  "mcpServers": {
    "brain-trust": {
      "url": "http://localhost:8000/mcp",
      "transport": "http",
      "env": {
        "OPENAI_API_KEY": "your_openai_api_key_here"
      }
    }
  }
}`,
      },
    ],
    verification: 'brain-trust tools should appear in Roo Code.',
  },

  zed: {
    name: 'Zed',
    description: 'Install brain-trust in Zed editor with HTTP transport.',
    steps: [
      {
        title: 'Start the server',
        description: 'Make sure Docker is running and start the brain-trust server:',
        code: 'docker-compose up -d',
      },
      {
        title: 'Configure Zed',
        description: 'Add to Zed MCP configuration:',
        code: `{
  "mcpServers": {
    "brain-trust": {
      "url": "http://localhost:8000/mcp",
      "transport": "http",
      "env": {
        "OPENAI_API_KEY": "your_openai_api_key_here"
      }
    }
  }
}`,
      },
    ],
    verification: 'Verify brain-trust is loaded in Zed MCP panel.',
  },

  claude_code: {
    name: 'Claude Code',
    description: 'Install brain-trust in Claude Code CLI with HTTP transport.',
    steps: [
      {
        title: 'Start the server',
        description: 'Make sure Docker is running and start the brain-trust server:',
        code: 'docker-compose up -d',
      },
      {
        title: 'Configure Claude Code',
        description: 'Add to Claude Code configuration:',
        code: `{
  "mcpServers": {
    "brain-trust": {
      "url": "http://localhost:8000/mcp",
      "transport": "http",
      "env": {
        "OPENAI_API_KEY": "your_openai_api_key_here"
      }
    }
  }
}`,
      },
    ],
    verification: 'brain-trust tools should be available in Claude Code CLI.',
  },
}
