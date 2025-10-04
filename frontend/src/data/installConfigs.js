export const installConfigs = {
  amazon_q: {
    name: 'Amazon Q Developer CLI',
    description: 'Add to your Amazon Q Developer CLI configuration file.',
    steps: [
      {
        title: 'Amazon Q CLI Config',
        description: 'Add this JSON block to your Amazon Q Developer CLI MCP config.',
        code: `{
  "mcpServers": {
    "ask-mcp": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp", "--api-key", "YOUR_API_KEY"]
    }
  }
}`,
      },
    ],
    verification: 'Restart the CLI and verify tools are listed.',
  },

  amp: {
    name: 'Amp',
    description: 'Configure Ask MCP in Amp.',
    steps: [
      {
        title: 'Amp Remote Server (HTTP)',
        description: 'With headers for model and max tokens.',
        code: `amp mcp add ask-mcp --header "X-OpenAI-API-Key=your_openai_api_key_here" --header "X-OpenAI-Model=gpt-4" --header "X-OpenAI-Max-Tokens=2000" https://ask-mcp.com/mcp`,
      },
    ],
    verification: 'Run a prompt and confirm tools are available.',
  },

  augment_code: {
    name: 'Augment Code',
    description: 'Add Ask MCP via UI or manual settings.',
    steps: [
      {
        title: 'Manual Configuration',
        description: 'Add to the augment.advanced settings JSON.',
        code: `"augment.advanced": {
  "mcpServers": [
    {
      "name": "ask-mcp",
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp", "--api-key", "YOUR_API_KEY"]
    }
  ]
}`,
      },
    ],
    verification: 'Restart Augment Code and verify tools appear.',
  },

  boltai: {
    name: 'BoltAI',
    description: 'Configure Ask MCP in BoltAI settings.',
    steps: [
      {
        title: 'BoltAI Settings JSON',
        description: 'Paste this JSON in Plugins settings.',
        code: `{
  "mcpServers": {
    "ask-mcp": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp", "--api-key", "YOUR_API_KEY"]
    }
  }
}`,
      },
    ],
    verification: 'Invoke an Ask MCP tool from BoltAI.',
  },

  claude_code: {
    name: 'Claude Code',
    description: 'Connect Claude Code CLI to Ask MCP using our hosted service.',
    steps: [
      {
        title: 'Claude Code (HTTP)',
        description: 'Add to Claude Code configuration:',
        code: `{
  "mcpServers": {
    "ask-mcp": {
      "type": "http",
      "url": "https://ask-mcp.com/mcp",
      "headers": {
        "X-OpenAI-API-Key": "your_openai_api_key_here",
        "X-OpenAI-Model": "gpt-4",
        "X-OpenAI-Max-Tokens": "2000"
      }
    }
  }
}`,
      },
    ],
    verification: 'Ask MCP tools should be available in Claude Code CLI.',
  },

  claude_desktop: {
    name: 'Claude Desktop',
    description: 'Connect Claude Desktop to Ask MCP using our hosted service.',
    steps: [
      {
        title: 'Configure Claude Desktop',
        description: 'Add to ~/Library/Application Support/Claude/.mcp.json (macOS) or %APPDATA%/Claude/.mcp.json (Windows):',
        code: `{
  "mcpServers": {
    "ask-mcp": {
      "type": "url",
      "url": "https://ask-mcp.com/mcp",
      "headers": {
        "X-OpenAI-API-Key": "your_openai_api_key_here",
        "X-OpenAI-Model": "gpt-4",
        "X-OpenAI-Max-Tokens": "2000"
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

  cline: {
    name: 'Cline',
    description: 'Connect Cline to Ask MCP using our hosted service.',
    steps: [
      {
        title: 'Configure Cline',
        description: 'Add to Cline MCP settings (cline_mcp_settings.json):',
        code: `{
  "mcpServers": {
    "ask-mcp": {
      "url": "https://ask-mcp.com/mcp",
      "headers": {
        "X-OpenAI-API-Key": "your_openai_api_key_here",
        "X-OpenAI-Model": "gpt-4",
        "X-OpenAI-Max-Tokens": "2000"
      },
      "disabled": false
    }
  }
}`,
      },
    ],
    verification: 'The Ask MCP tools should be available in Cline.',
  },

  copilot_coding_agent: {
    name: 'Copilot Coding Agent',
    description: 'Add Ask MCP to GitHub Copilot Coding Agent MCP config.',
    steps: [
      {
        title: 'Copilot Coding Agent',
        description: 'Add to Copilot Coding Agent configuration.',
        code: `{
  "mcpServers": {
    "ask-mcp": {
      "type": "http",
      "url": "https://ask-mcp.com/mcp",
      "headers": {
        "X-OpenAI-API-Key": "your_openai_api_key_here",
        "X-OpenAI-Model": "gpt-4",
        "X-OpenAI-Max-Tokens": "2000"
      },
      "tools": ["phone_a_friend", "review_plan", "health_check"]
    }
  }
}`,
      },
    ],
    verification: 'Verify Ask MCP appears in Copilot Coding Agent tools.',
  },

  crush: {
    name: 'Crush',
    description: 'Configure Ask MCP in Crush.',
    steps: [
      {
        title: 'Crush HTTP',
        description: 'Add to crush.json.',
        code: `{
  "$schema": "https://charm.land/crush.json",
  "mcp": {
    "ask-mcp": {
      "type": "http",
      "url": "https://ask-mcp.com/mcp",
      "headers": {
        "X-OpenAI-API-Key": "your_openai_api_key_here",
        "X-OpenAI-Model": "gpt-4",
        "X-OpenAI-Max-Tokens": "2000"
      }
    }
  }
}`,
      },
    ],
    verification: 'Restart Crush and check the MCP list.',
  },

  cursor: {
    name: 'Cursor',
    description: 'Connect Cursor IDE to Ask MCP using our hosted service.',
    installButton: 'https://cursor.com/en/install-mcp?name=ask-mcp&config=eyJ1cmwiOiJodHRwczovL2Fzay1tY3AuY29tL21jcCIsImhlYWRlcnMiOnsiWC1PcGVuQUktQVBJLUtleSI6InlvdXJfb3BlbmFpX2FwaV9rZXlfaGVyZSIsIlgtT3BlbkFJLU1vZGVsIjoiZ3B0LTQiLCJYLU9wZW5BSS1NYXgtVG9rZW5zIjoiMjAwMCJ9fQ%3D%3D',
    steps: [
      {
        title: 'Configure Cursor',
        description: 'Add to ~/.cursor/mcp.json:',
        code: `{
  "mcpServers": {
    "ask-mcp": {
      "url": "https://ask-mcp.com/mcp",
      "headers": {
        "X-OpenAI-API-Key": "your_openai_api_key_here",
        "X-OpenAI-Model": "gpt-4",
        "X-OpenAI-Max-Tokens": "2000"
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

  docker: {
    name: 'Docker (client)',
    description: 'Example launching a local MCP server via Docker (pattern only).',
    steps: [
      {
        title: 'Example Docker client config',
        description: 'Adjust to your client’s format; our service is remote HTTP.',
        code: `{
  "mcpServers": {
    "ask-mcp": {
      "command": "docker",
      "args": ["run", "-i", "--rm", "your-mcp-image"],
      "type": "stdio"
    }
  }
}`,
      },
    ],
    verification: 'Confirm tools load when starting via Docker.',
  },

  gemini_cli: {
    name: 'Gemini CLI',
    description: 'Add Ask MCP to Gemini CLI settings (~/.gemini/settings.json).',
    steps: [
      {
        title: 'Gemini CLI Remote',
        description: 'Add to ~/.gemini/settings.json.',
        code: `{
  "mcpServers": {
    "ask-mcp": {
      "httpUrl": "https://ask-mcp.com/mcp",
      "headers": {
        "X-OpenAI-API-Key": "your_openai_api_key_here",
        "X-OpenAI-Model": "gpt-4",
        "X-OpenAI-Max-Tokens": "2000",
        "Accept": "application/json, text/event-stream"
      }
    }
  }
}`,
      },
    ],
    verification: 'Run a Gemini CLI chat and verify tools are present.',
  },

  jetbrains_ai: {
    name: 'JetBrains AI Assistant',
    description: 'Add Ask MCP via the AI Assistant MCP pane.',
    steps: [
      {
        title: 'Add as JSON',
        description: 'Paste configuration as JSON in Add MCP dialog.',
        code: `{
  "mcpServers": {
    "ask-mcp": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp", "--api-key", "YOUR_API_KEY"]
    }
  }
}`,
      },
    ],
    verification: 'Apply and check tools in AI Assistant.',
  },

  kiro: {
    name: 'Kiro',
    description: 'Add Ask MCP in Kiro MCP Servers.',
    steps: [
      {
        title: 'Kiro JSON',
        description: 'Add an entry to Kiro MCP servers.',
        code: `{
  "mcpServers": {
    "ask-mcp": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp", "--api-key", "YOUR_API_KEY"],
      "disabled": false,
      "autoApprove": []
    }
  }
}`,
      },
    ],
    verification: 'Save and verify Ask MCP is available in Kiro.',
  },

  lm_studio: {
    name: 'LM Studio',
    description: 'Configure Ask MCP in LM Studio MCP settings.',
    installButton: 'https://lmstudio.ai/install-mcp?name=ask-mcp&config=eyJjb21tYW5kIjoibnB4IiwiYXJncyI6WyIteSIsIkB1cHN0YXNoL2NvbnRleHQ3LW1jcEBsYXRlc3QiXX0%3D',
    steps: [
      {
        title: 'LM Studio Manual',
        description: 'Edit mcp.json via Program > Install > Edit mcp.json.',
        code: `{
  "mcpServers": {
    "ask-mcp": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp", "--api-key", "YOUR_API_KEY"]
    }
  }
}`,
      },
    ],
    verification: 'Toggle the MCP server in LM Studio and test.',
  },

  opencode: {
    name: 'Opencode',
    description: 'Add Ask MCP to Opencode settings.',
    steps: [
      {
        title: 'Opencode Remote',
        description: 'Add to Opencode MCP configuration.',
        code: `{
  "mcp": {
    "ask-mcp": {
      "type": "remote",
      "url": "https://ask-mcp.com/mcp",
      "headers": {
        "X-OpenAI-API-Key": "your_openai_api_key_here",
        "X-OpenAI-Model": "gpt-4",
        "X-OpenAI-Max-Tokens": "2000"
      },
      "enabled": true
    }
  }
}`,
      },
    ],
    verification: 'Restart Opencode and verify.',
  },

  openai_codex: {
    name: 'OpenAI Codex',
    description: 'Example local server configuration for Codex.',
    steps: [
      {
        title: 'Codex TOML',
        description: 'Add to Codex MCP server settings (TOML).',
        code: `[mcp_servers.ask-mcp]
command = "npx"
args = ["-y", "@upstash/context7-mcp", "--api-key", "YOUR_API_KEY"]`,
      },
    ],
    verification: 'Restart Codex and verify.',
  },

  perplexity_desktop: {
    name: 'Perplexity Desktop',
    description: 'Add Ask MCP via Connectors > Add Connector > Advanced.',
    steps: [
      {
        title: 'Perplexity Connector JSON',
        description: 'Paste in the advanced connector JSON.',
        code: `{
  "command": "npx",
  "args": ["-y", "@upstash/context7-mcp", "--api-key", "YOUR_API_KEY"],
  "env": {}
}`,
      },
    ],
    verification: 'Save and verify tools are usable.',
  },

  qodo_gen: {
    name: 'Qodo Gen',
    description: 'Add Ask MCP to Qodo Gen MCP list (VSCode/IntelliJ panels).',
    steps: [
      {
        title: 'Qodo Gen Local',
        description: 'Local server connection.',
        code: `{
  "mcpServers": {
    "ask-mcp": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp", "--api-key", "YOUR_API_KEY"]
    }
  }
}`,
      },
      {
        title: 'Qodo Gen Remote',
        description: 'Remote server connection.',
        code: `{
  "mcpServers": {
    "ask-mcp": {
      "url": "https://ask-mcp.com/mcp"
    }
  }
}`,
      },
    ],
    verification: 'Connect more tools and select Ask MCP.',
  },

  roo_code: {
    name: 'Roo Code',
    description: 'Connect Roo Code to Ask MCP using our hosted service.',
    steps: [
      {
        title: 'Roo Code Remote',
        description: 'Add to Roo Code MCP settings.',
        code: `{
  "mcpServers": {
    "ask-mcp": {
      "type": "streamable-http",
      "url": "https://ask-mcp.com/mcp",
      "headers": {
        "X-OpenAI-API-Key": "your_openai_api_key_here",
        "X-OpenAI-Model": "gpt-4",
        "X-OpenAI-Max-Tokens": "2000"
      }
    }
  }
}`,
      },
    ],
    verification: 'Ask MCP tools should appear in Roo Code.',
  },

  rovo_dev_cli: {
    name: 'Rovo Dev CLI',
    description: 'Add Ask MCP via the Rovo Dev CLI MCP config.',
    steps: [
      {
        title: 'Rovo Dev CLI Remote',
        description: 'Edit configuration via CLI and add the server URL.',
        code: `{
  "mcpServers": {
    "ask-mcp": {
      "url": "https://ask-mcp.com/mcp"
    }
  }
}`,
      },
    ],
    verification: 'Confirm tools in Rovo Dev CLI.',
  },

  smithery: {
    name: 'Smithery',
    description: 'Install Ask MCP via Smithery for supported clients.',
    installButton: 'https://smithery.ai/server/@upstash/context7-mcp',
    steps: [
      {
        title: 'Smithery Install',
        description: 'Use Smithery CLI to install.',
        code: `npx -y @smithery/cli@latest install @upstash/context7-mcp --client <CLIENT_NAME> --key <YOUR_SMITHERY_KEY>`,
      },
    ],
    verification: 'Open your client and verify installation.',
  },

  trae: {
    name: 'Trae',
    description: 'Add Ask MCP configuration to Trae.',
    steps: [
      {
        title: 'Trae Remote',
        description: 'Add a remote server entry.',
        code: `{
  "mcpServers": {
    "ask-mcp": {
      "url": "https://ask-mcp.com/mcp"
    }
  }
}`,
      },
    ],
    verification: 'Save and confirm connector is active.',
  },

  vscode: {
    name: 'VS Code',
    description: 'Configure MCP servers via VS Code (Copilot Chat MCP).',
    installButton: 'https://insiders.vscode.dev/redirect?url=vscode%3Amcp%2Finstall%3F%7B%22name%22%3A%22ask-mcp%22%2C%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22@upstash/context7-mcp@latest%22%5D%7D',
    steps: [
      {
        title: 'VS Code HTTP',
        description: 'Add to VS Code MCP settings (settings.json).',
        code: `"mcp": {
  "servers": {
    "ask-mcp": {
      "type": "http",
      "url": "https://ask-mcp.com/mcp",
      "headers": {
        "X-OpenAI-API-Key": "your_openai_api_key_here",
        "X-OpenAI-Model": "gpt-4",
        "X-OpenAI-Max-Tokens": "2000"
      }
    }
  }
}`,
      },
    ],
    verification: 'Open Copilot Chat and verify Ask MCP tools.',
  },

  warp: {
    name: 'Warp',
    description: 'Add Ask MCP through Warp settings.',
    steps: [
      {
        title: 'Warp MCP JSON',
        description: 'Add via Settings > AI > Manage MCP servers.',
        code: `{
  "ask-mcp": {
    "command": "npx",
    "args": ["-y", "@upstash/context7-mcp", "--api-key", "YOUR_API_KEY"],
    "start_on_launch": true
  }
}`,
      },
    ],
    verification: 'Save and verify from Warp UI.',
  },

  visual_studio_2022: {
    name: 'Visual Studio 2022',
    description: 'Add Ask MCP to Visual Studio MCP Servers settings.',
    steps: [
      {
        title: 'Visual Studio HTTP',
        description: 'Add to Visual Studio MCP config file.',
        code: `{
  "inputs": [],
  "servers": {
    "ask-mcp": {
      "type": "http",
      "url": "https://ask-mcp.com/mcp",
      "headers": {
        "X-OpenAI-API-Key": "your_openai_api_key_here",
        "X-OpenAI-Model": "gpt-4",
        "X-OpenAI-Max-Tokens": "2000"
      }
    }
  }
}`,
      },
    ],
    verification: 'Apply and verify Ask MCP is available.',
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
      "serverUrl": "https://ask-mcp.com/mcp",
      "headers": {
        "X-OpenAI-API-Key": "your_openai_api_key_here",
        "X-OpenAI-Model": "gpt-4",
        "X-OpenAI-Max-Tokens": "2000"
      }
    }
  }
}`,
      },
    ],
    verification: 'Check Windsurf MCP panel for Ask MCP connection.',
  },

  zencoder: {
    name: 'Zencoder',
    description: 'Add Ask MCP via the Add custom MCP dialog.',
    steps: [
      {
        title: 'Zencoder JSON',
        description: 'Paste command and args JSON.',
        code: `{
  "command": "npx",
  "args": ["-y", "@upstash/context7-mcp", "--api-key", "YOUR_API_KEY"]
}`,
      },
    ],
    verification: 'Click Install and confirm.',
  },
}
export const installConfigsDeprecated = {
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
        description: 'Add to ~/Library/Application Support/Claude/.mcp.json (macOS) or %APPDATA%/Claude/.mcp.json (Windows):',
        code: `{
  "mcpServers": {
    "ask-mcp": {
      "type": "url",
      "url": "https://ask-mcp.com/mcp",
      "headers": {
        "X-OpenAI-API-Key": "your_openai_api_key_here"
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
      "headers": {
        "X-OpenAI-API-Key": "your_openai_api_key_here"
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
        description: 'Add to Cline MCP settings (cline_mcp_settings.json):',
        code: `{
  "mcpServers": {
    "ask-mcp": {
      "url": "https://ask-mcp.com/mcp",
      "headers": {
        "X-OpenAI-API-Key": "your_openai_api_key_here"
      },
      "disabled": false
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
      "headers": {
        "X-OpenAI-API-Key": "your_openai_api_key_here"
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
      "headers": {
        "X-OpenAI-API-Key": "your_openai_api_key_here"
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
        description: 'Zed connects via Claude Code ACP / project .mcp.json. Add a project-level .mcp.json:',
        code: `{
  "mcpServers": {
    "ask-mcp": {
      "type": "url",
      "url": "https://ask-mcp.com/mcp",
      "headers": {
        "X-OpenAI-API-Key": "your_openai_api_key_here"
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
      "headers": {
        "X-OpenAI-API-Key": "your_openai_api_key_here"
      }
    }
  }
}`,
      },
    ],
    verification: 'Ask MCP tools should be available in Claude Code CLI.',
  },
}
