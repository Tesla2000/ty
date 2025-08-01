# Editor settings

The editor settings supported by ty's language server, as well as the settings specific to [ty's VS Code extension](https://github.com/astral-sh/ty-vscode/).

## `python.ty.disableLanguageServices`

Whether to disable the language services for the ty language server like code completion, hover,
go to definition, etc.

This is useful if you want to use ty exclusively for type checking and want to use another language
server for features like code completion, hover, go to definition, etc.

**Default value**: `false`

**Type**: `boolean`

**Example usage**:

```json
{
  "python.ty.disableLanguageServices": true
}
```

## `diagnosticMode`

Determines the scope of the diagnostics reported by the language server.

- `openFilesOnly`: Diagnostics are reported only for files that are currently open in the editor.
- `workspace`: Diagnostics are reported for all files in the workspace.

**Default value**: `"openFilesOnly"`

**Type**: `"workspace" | "openFilesOnly"`

**Example usage**:

```json
{
  "ty.diagnosticMode": "workspace"
}
```

## `logFile`

Path to the file to which the language server writes its log messages. By default, ty writes log messages to stderr.

**Default value**: `null`

**Type**: `string`

**Example usage**:

```json
{
  "ty.logFile": "~/path/to/ty.log"
}
```

## `logLevel`

The log level to use for the language server.

**Default value**: `"info"`

**Type**: `"trace" | "debug" | "info" | "warn" | "error"`

**Example usage**:

```json
{
  "ty.logLevel": "debug"
}
```

## `trace.server`

The detail level at which messages between the language server and the editor (client) are logged. Refer to the [LSP
specification](https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#traceValue)
for more information.

**Default value**: `"off"`

**Type**: `"off" | "messages" | "verbose"`

**Example usage**:

```json
{
  "ty.trace.server": "messages"
}
```

## VS Code specific

The following settings are specific to ty's VS Code extension.

### `importStrategy`

Strategy for loading the `ty` executable.

- `fromEnvironment` finds ty in the environment, falling back to the bundled version
- `useBundled` uses the version bundled with the extension

**Default value**: `"fromEnvironment"`

**Type**: `"fromEnvironment" | "useBundled"`

**Example usage**:

```json
{
  "ty.importStrategy": "useBundled"
}
```

### `interpreter`

A list of paths to Python interpreters. Even though this is a list, only the first interpreter is
used.

The interpreter path is used to find the `ty` executable when
[`ty.importStrategy`](#importstrategy) is set to `fromEnvironment`.

**Default value**: `[]`

**Type**: `string[]`

**Example usage**:

```json
{
  "ty.interpreter": ["/home/user/.local/bin/python"]
}
```

### `path`

A list of path to `ty` executables.

The extension uses the first executable that exists. This setting takes precedence over the
[`ty.importStrategy`](#importstrategy) setting.

**Default value**: `[]`

**Type**: `string[]`

**Example usage**:

```json
{
  "ty.path": ["/home/user/.local/bin/ty"]
}
```
