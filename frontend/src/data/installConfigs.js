export const installConfigs = {
  cursor: {
    name: 'Cursor',
    description: 'Connect Cursor IDE to Ask MCP using our hosted service.',
    installButton: 'https://cursor.com/en/install-mcp?name=ask-mcp&config=eyJ1cmwiOiAiaHR0cHM6Ly9hc2stbWNwLmNvbS9tY3AiLCAidHJhbnNwb3J0IjogImh0dHAiLCAiZW52IjogeyJPUEVOQUlfQVBJX0tFWSI6ICJ5b3VyX29wZW5haV9hcGlfa2V5X2hlcmUifX0=',
    steps: [
      {
        title: 'Configure Cursor',
        description: 'Add to ~/.cursor/mcp.json:',
        code: `{
  "mcpServers": {
    "ask-mcp": {
      "url": "https://ask-mcp.com/mcp",
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
        description: 'Restart Cursor to load the Ask MCP server configuration.',
      },
    ],
    verification: 'Try asking: "Use phone_a_friend to ask: What is FastMCP?"',
  },

  claude_desktop: {
    name: 'Claude Desktop',
    description: 'Connect Claude Desktop to Ask MCP using our hosted service.',
    steps: [
      {
        title: 'Configure Claude Desktop',
        description: 'Add to ~/Library/Application Support/Claude/claude_desktop_config.json (Mac) or %APPDATA%/Claude/claude_desktop_config.json (Windows):',
        code: `{
  "mcpServers": {
    "ask-mcp": {
      "url": "https://ask-mcp.com/mcp",
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
        description: 'Restart Claude Desktop to load the Ask MCP server.',
      },
    ],
    verification: 'The Ask MCP tools should appear in the Claude Desktop interface.',
  },

  vscode: {
    name: 'VS Code',
    description: 'Connect VS Code to Ask MCP using the MCP extension and our hosted service.',
    steps: [
      {
        title: 'Install MCP Extension',
        description: 'Install the Model Context Protocol extension from the VS Code marketplace.',
      },
      {
        title: 'Configure MCP Extension',
        description: 'Add to .vscode/mcp.json in your workspace:',
        code: `{
  "mcpServers": {
    "ask-mcp": {
      "url": "https://ask-mcp.com/mcp",
      "transport": "http",
      "env": {
        "OPENAI_API_KEY": "your_openai_api_key_here"
      }
    }
  }
}`,
      },
    ],
    verification: 'Check the MCP extension panel to see if Ask MCP is connected.',
  },

  cline: {
    name: 'Cline',
    description: 'Connect Cline to Ask MCP using our hosted service.',
    steps: [
      {
        title: 'Configure Cline',
        description: 'Add to Cline MCP settings:',
        code: `{
  "mcpServers": {
    "ask-mcp": {
      "url": "https://ask-mcp.com/mcp",
      "transport": "http",
      "env": {
        "OPENAI_API_KEY": "your_openai_api_key_here"
      }
    }
  }
}`,
      },
    ],
    verification: 'The Ask MCP tools should be available in Cline.',
  },

  windsurf: {
    name: 'Windsurf',
    description: 'Connect Windsurf IDE to Ask MCP using our hosted service.',
    steps: [
      {
        title: 'Configure Windsurf',
        description: 'Add to Windsurf MCP configuration:',
        code: `{
  "mcpServers": {
    "ask-mcp": {
      "url": "https://ask-mcp.com/mcp",
      "transport": "http",
      "env": {
        "OPENAI_API_KEY": "your_openai_api_key_here"
      }
    }
  }
}`,
      },
    ],
    verification: 'Check Windsurf MCP panel for Ask MCP connection.',
  },

  roo_code: {
    name: 'Roo Code',
    description: 'Connect Roo Code to Ask MCP using our hosted service.',
    steps: [
      {
        title: 'Configure Roo Code',
        description: 'Add to Roo Code MCP settings:',
        code: `{
  "mcpServers": {
    "ask-mcp": {
      "url": "https://ask-mcp.com/mcp",
      "transport": "http",
      "env": {
        "OPENAI_API_KEY": "your_openai_api_key_here"
      }
    }
  }
}`,
      },
    ],
    verification: 'Ask MCP tools should appear in Roo Code.',
  },

  zed: {
    name: 'Zed',
    description: 'Connect Zed editor to Ask MCP using our hosted service.',
    steps: [
      {
        title: 'Configure Zed',
        description: 'Add to Zed MCP configuration:',
        code: `{
  "mcpServers": {
    "ask-mcp": {
      "url": "https://ask-mcp.com/mcp",
      "transport": "http",
      "env": {
        "OPENAI_API_KEY": "your_openai_api_key_here"
      }
    }
  }
}`,
      },
    ],
    verification: 'Verify Ask MCP is loaded in Zed MCP panel.',
  },

  claude_code: {
    name: 'Claude Code',
    description: 'Connect Claude Code CLI to Ask MCP using our hosted service.',
    steps: [
      {
        title: 'Configure Claude Code',
        description: 'Add to Claude Code configuration:',
        code: `{
  "mcpServers": {
    "ask-mcp": {
      "url": "https://ask-mcp.com/mcp",
      "transport": "http",
      "env": {
        "OPENAI_API_KEY": "your_openai_api_key_here"
      }
    }
  }
}`,
      },
    ],
    verification: 'Ask MCP tools should be available in Claude Code CLI.',
  },
}
