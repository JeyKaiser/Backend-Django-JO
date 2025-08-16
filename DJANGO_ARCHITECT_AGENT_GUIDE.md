# Django Backend Architecture Agent Configuration Guide

## Overview

This guide explains how to create and use specialized Claude Code agents for Django backend architecture and database design. Two specialized agents have been configured for your JO System platform:

1. **django-architect** - General Django backend architecture specialist (user-level)
2. **jo-system-architect** - Project-specific fashion platform specialist (project-level)

## Agent Locations

```
~/.claude/agents/django-architect.md          # User-level (available across all projects)
./.claude/agents/jo-system-architect.md       # Project-level (specific to this project)
```

## Agent Capabilities

### django-architect (General Django Specialist)
- **Focus:** Django models, database design, API architecture, scalability patterns
- **Expertise:** Model relationships, query optimization, DRF patterns, migration strategies
- **Tools:** Read, Edit, MultiEdit, Glob, Grep, LS, Bash
- **Use Case:** General Django backend architecture questions and improvements

### jo-system-architect (JO System Specialist)  
- **Focus:** Fashion industry-specific backend architecture for the JO platform
- **Expertise:** Collection management, SAP integration, fashion workflow optimization
- **Tools:** Read, Edit, MultiEdit, Glob, Grep, LS, Bash, Write
- **Use Case:** Platform-specific improvements and feature development

## How to Use the Agents

### Method 1: Direct Agent Invocation
Use the `@agent-name` syntax to invoke a specific agent:

```
@django-architect Please analyze the Collection model relationships and suggest improvements for better query performance.
```

```
@jo-system-architect How can we optimize the SAP integration for fabric data synchronization?
```

### Method 2: Implicit Agent Selection
Claude Code will automatically select the appropriate agent based on your request context:

```
# This will likely trigger django-architect
"Analyze the Django models and suggest database optimizations"

# This will likely trigger jo-system-architect  
"How can we improve the collection workflow for the fashion team?"
```

## Sample Use Cases

### Database Architecture Review
```
@django-architect Review the models.py files and identify:
1. Potential relationship improvements
2. Missing database indexes
3. Cascade strategy inconsistencies
4. Performance optimization opportunities
```

### API Optimization
```
@django-architect Analyze the views.py structure and suggest:
1. ViewSet optimization patterns
2. Serializer improvements for complex relationships
3. Query optimization for collection endpoints
4. Caching strategies for frequently accessed data
```

### Fashion Platform Enhancements
```
@jo-system-architect Design a solution for:
1. Real-time collection status updates for the creative team
2. Improved fabric search and filtering capabilities
3. Integration patterns for new SAP modules
4. Audit trail for design decision tracking
```

### Migration Planning
```
@django-architect Plan database migrations for:
1. Adding proper indexes to Collection and Tela models
2. Optimizing foreign key relationships
3. Implementing soft delete patterns for archived collections
4. Adding database constraints for data integrity
```

## Configuration Details

### Agent Configuration Structure
Each agent is defined with YAML frontmatter:

```yaml
---
name: agent-name
description: What this agent specializes in and when to use it
tools: Comma-separated list of available tools
---

System prompt defining the agent's expertise and approach...
```

### Tool Permissions
Both agents have access to:
- **Read/Edit/MultiEdit:** For code analysis and modifications
- **Glob/Grep:** For codebase exploration and pattern searching  
- **LS/Bash:** For file system operations and command execution
- **Write:** (jo-system-architect only) For creating new files when needed

## Best Practices

### When to Use Each Agent

**Use django-architect for:**
- General Django best practices questions
- Database design and optimization
- Model relationship analysis
- API architecture improvements
- Migration planning
- Performance optimization

**Use jo-system-architect for:**
- Platform-specific feature development
- Fashion industry workflow optimizations
- SAP integration improvements
- Collection management enhancements
- Domain-specific architectural decisions

### Effective Agent Communication

1. **Be Specific:** Provide clear context about what you want to accomplish
2. **Include Files:** Mention specific files or modules you want analyzed
3. **Define Scope:** Clarify whether you want analysis, recommendations, or implementation
4. **Request Examples:** Ask for code examples when requesting architectural changes

## Example Workflows

### Complete Model Analysis Workflow
```
1. @django-architect Analyze all models.py files and create a relationship diagram
2. @django-architect Identify performance bottlenecks in current model design
3. @django-architect Propose optimized model structure with migrations
4. @jo-system-architect Validate proposed changes against fashion workflow requirements
5. @django-architect Implement the approved model changes
```

### API Enhancement Workflow  
```
1. @django-architect Review current API structure in views.py
2. @jo-system-architect Analyze API usage patterns from frontend perspective
3. @django-architect Design improved ViewSet architecture
4. @jo-system-architect Implement platform-specific API enhancements
5. @django-architect Add comprehensive API documentation
```

## Advanced Configuration

### Customizing Agent Behavior
You can modify the agent configurations by editing the `.md` files:
- Update the system prompt to add new expertise areas
- Modify tool permissions for security or functionality needs
- Adjust the description to refine automatic agent selection

### Creating Additional Agents
Follow the same pattern to create specialized agents for:
- Frontend integration (`frontend-integration-specialist`)
- DevOps and deployment (`jo-devops-specialist`)
- Data analytics (`fashion-data-analyst`)
- API testing (`api-testing-specialist`)

## Troubleshooting

### Agent Not Found
- Verify the agent file exists in the correct location
- Check YAML frontmatter syntax for errors
- Ensure proper file permissions

### Wrong Agent Selected
- Use explicit `@agent-name` syntax for specific agent selection
- Adjust agent descriptions to better define their use cases
- Check for conflicting agent descriptions

### Tool Permission Errors
- Review the tools list in agent configuration
- Ensure requested operations match available tools
- Check file system permissions for file operations

## Next Steps

1. Test both agents with sample architecture questions
2. Refine agent descriptions based on usage patterns
3. Create additional specialized agents as needed
4. Establish team conventions for agent usage
5. Document domain-specific architectural decisions for future reference

The agents are now ready to help you build and optimize your Django backend architecture with both general best practices and platform-specific expertise.