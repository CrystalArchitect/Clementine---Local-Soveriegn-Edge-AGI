
// this file is generated — do not edit it


/// <reference types="@sveltejs/kit" />

/**
 * This module provides access to environment variables that are injected _statically_ into your bundle at build time and are limited to _private_ access.
 * 
 * |         | Runtime                                                                    | Build time                                                               |
 * | ------- | -------------------------------------------------------------------------- | ------------------------------------------------------------------------ |
 * | Private | [`$env/dynamic/private`](https://svelte.dev/docs/kit/$env-dynamic-private) | [`$env/static/private`](https://svelte.dev/docs/kit/$env-static-private) |
 * | Public  | [`$env/dynamic/public`](https://svelte.dev/docs/kit/$env-dynamic-public)   | [`$env/static/public`](https://svelte.dev/docs/kit/$env-static-public)   |
 * 
 * Static environment variables are [loaded by Vite](https://vitejs.dev/guide/env-and-mode.html#env-files) from `.env` files and `process.env` at build time and then statically injected into your bundle at build time, enabling optimisations like dead code elimination.
 * 
 * **_Private_ access:**
 * 
 * - This module cannot be imported into client-side code
 * - This module only includes variables that _do not_ begin with [`config.kit.env.publicPrefix`](https://svelte.dev/docs/kit/configuration#env) _and do_ start with [`config.kit.env.privatePrefix`](https://svelte.dev/docs/kit/configuration#env) (if configured)
 * 
 * For example, given the following build time environment:
 * 
 * ```env
 * ENVIRONMENT=production
 * PUBLIC_BASE_URL=http://site.com
 * ```
 * 
 * With the default `publicPrefix` and `privatePrefix`:
 * 
 * ```ts
 * import { ENVIRONMENT, PUBLIC_BASE_URL } from '$env/static/private';
 * 
 * console.log(ENVIRONMENT); // => "production"
 * console.log(PUBLIC_BASE_URL); // => throws error during build
 * ```
 * 
 * The above values will be the same _even if_ different values for `ENVIRONMENT` or `PUBLIC_BASE_URL` are set at runtime, as they are statically replaced in your code with their build time values.
 */
declare module '$env/static/private' {
	export const SVELTEKIT_FORK: string;
	export const NODE_ENV: string;
	export const INIT_CWD: string;
	export const CARGO_HTTP_CAINFO: string;
	export const ANT_IMAGE_REPOSITORY: string;
	export const npm_command: string;
	export const USE_SHTTP_MCP: string;
	export const ENV_MANAGER_ENABLE_DIAG_LOGS: string;
	export const IS_SANDBOX: string;
	export const npm_config_global_prefix: string;
	export const CLAUDE_CODE_EXECPATH: string;
	export const PWD: string;
	export const JAVA_HOME: string;
	export const npm_config_init_module: string;
	export const npm_config_globalconfig: string;
	export const CLOUDSDK_PROXY_PORT: string;
	export const CLOUDSDK_PROXY_ADDRESS: string;
	export const FSSPEC_GCS: string;
	export const https_proxy: string;
	export const CLAUDE_ADDITIONAL_DIRECTORIES: string;
	export const HOME: string;
	export const DOCUMENTS_MCP_SCRATCH_ROOT: string;
	export const HEX_CACERTS_PATH: string;
	export const CLAUDE_CODE_WEBSOCKET_AUTH_FILE_DESCRIPTOR: string;
	export const JAVA_TOOL_OPTIONS: string;
	export const npm_config_user_agent: string;
	export const PYTHONUNBUFFERED: string;
	export const CLAUDE_CODE_CONTAINER_ID: string;
	export const AI_AGENT: string;
	export const RUSTUP_HOME: string;
	export const npm_package_json: string;
	export const CLAUDE_CODE_TEE_SDK_STDOUT: string;
	export const no_proxy: string;
	export const CLAUDE_CODE_POST_FOR_SESSION_INGRESS_V2: string;
	export const CCR_SPAWN_TIMESTAMP_MS: string;
	export const CLAUDE_SESSION_INGRESS_TOKEN_FILE: string;
	export const OLDPWD: string;
	export const NO_PROXY: string;
	export const CLAUDE_CODE_REMOTE_SEND_KEEPALIVES: string;
	export const GIT_CONFIG_VALUE_2: string;
	export const npm_config_userconfig: string;
	export const CLOUDSDK_AUTH_ACCESS_TOKEN: string;
	export const RBENV_ROOT: string;
	export const UV_NATIVE_TLS: string;
	export const GRPC_DEFAULT_SSL_ROOTS_FILE_PATH: string;
	export const CCR_AGENT_PROXY_ENABLED: string;
	export const CLAUDE_CODE_USE_CCR_V2: string;
	export const GIT_EDITOR: string;
	export const GLOBAL_AGENT_HTTPS_PROXY: string;
	export const ANT_IMAGE_TAG: string;
	export const npm_config_https_proxy: string;
	export const AWS_CA_BUNDLE: string;
	export const CLAUDE_CODE_USER_EMAIL: string;
	export const NODE_EXTRA_CA_CERTS: string;
	export const GITHUB_TOKEN: string;
	export const CLAUDE_CODE_SYNC_SKILLS: string;
	export const CCR_EGRESS_GATEWAY_ENABLED: string;
	export const CLAUDE_ENABLE_STREAM_WATCHDOG: string;
	export const npm_lifecycle_event: string;
	export const NODE_OPTIONS: string;
	export const CLAUDE_CODE_BASE_REF: string;
	export const REQUESTS_CA_BUNDLE: string;
	export const CCR_ENABLE_TRACING: string;
	export const CLAUDE_CODE_DEBUG: string;
	export const npm_config_prefix: string;
	export const GCM_INTERACTIVE: string;
	export const COLOR: string;
	export const CLAUDE_CODE_ENVIRONMENT_RUNNER_VERSION: string;
	export const GIT_ASKPASS: string;
	export const CCR_SETTINGS_JSON_OVERLAY: string;
	export const CLAUDE_CODE_REMOTE_SESSION_ID: string;
	export const USE_BUILTIN_RIPGREP: string;
	export const CLAUDE_CODE_DIAGNOSTICS_FILE: string;
	export const BUN_INSTALL: string;
	export const DOCKER_HTTPS_PROXY: string;
	export const ANTHROPIC_BASE_URL: string;
	export const GH_TOKEN: string;
	export const SHLVL: string;
	export const EDITOR: string;
	export const CLOUDSDK_CORE_CUSTOM_CA_CERTS_FILE: string;
	export const GIT_SSL_CAINFO: string;
	export const CLAUDE_CODE_REMOTE: string;
	export const npm_config_npm_version: string;
	export const npm_config_cache: string;
	export const NODE: string;
	export const TERM: string;
	export const CLAUDE_CODE_ACCOUNT_UUID: string;
	export const SKIP_PLUGIN_MARKETPLACE: string;
	export const GIT_CONFIG_VALUE_0: string;
	export const MCP_TOOL_TIMEOUT: string;
	export const MCP_CONNECTION_NONBLOCKING: string;
	export const npm_config_node_gyp: string;
	export const SHELL: string;
	export const HTTPS_PROXY: string;
	export const PATH: string;
	export const DENO_TLS_CA_STORE: string;
	export const GIT_CONFIG_COUNT: string;
	export const CLAUDE_CODE_OAUTH_TOKEN_FILE_DESCRIPTOR: string;
	export const MAX_THINKING_TOKENS: string;
	export const GIT_CONFIG_VALUE_1: string;
	export const npm_config_local_prefix: string;
	export const npm_package_name: string;
	export const YARN_HTTPS_PROXY: string;
	export const CLAUDE_CODE_VERSION: string;
	export const GIT_CONFIG_KEY_2: string;
	export const COREPACK_ENABLE_AUTO_PIN: string;
	export const npm_config_noproxy: string;
	export const PLAYWRIGHT_BROWSERS_PATH: string;
	export const CCR_UPSTREAM_PROXY_ENABLED: string;
	export const npm_execpath: string;
	export const SSL_CERT_FILE: string;
	export const CLAUDE_AUTO_BACKGROUND_TASKS: string;
	export const CLAUDE_AFTER_LAST_COMPACT: string;
	export const CLAUDE_CODE_ORGANIZATION_UUID: string;
	export const CLOUDSDK_PROXY_TYPE: string;
	export const CLAUDE_CODE_ENTRYPOINT: string;
	export const ENVRUNNER_SKIP_ACK: string;
	export const CLAUDE_CODE_PROVIDER_MANAGED_BY_HOST: string;
	export const CLAUDE_CODE_PROXY_RESOLVES_HOSTS: string;
	export const CLAUDE_PID: string;
	export const NoDefaultCurrentDirectoryInExePath: string;
	export const CLAUDE_EFFORT: string;
	export const TRACEPARENT: string;
	export const CLAUDE_CODE_DISABLE_BUILTIN_ANTMCP: string;
	export const DENO_CERT: string;
	export const npm_package_version: string;
	export const CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD: string;
	export const CLAUDE_CODE_WORKER_EPOCH: string;
	export const HTTPLIB2_CA_CERTS: string;
	export const npm_node_execpath: string;
	export const DEBIAN_FRONTEND: string;
	export const CLAUDECODE: string;
	export const ELECTRON_GET_USE_PROXY: string;
	export const PIP_CERT: string;
	export const CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE: string;
	export const npm_lifecycle_script: string;
	export const CLAUDE_CODE_CHILD_SESSION: string;
	export const CLAUDE_AUTOCOMPACT_PCT_OVERRIDE: string;
	export const CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH: string;
	export const CCR_TEST_GITPROXY: string;
	export const AWS_SECRET_ACCESS_KEY: string;
	export const CURL_CA_BUNDLE: string;
	export const RUST_BACKTRACE: string;
	export const GLOBAL_AGENT_NO_PROXY: string;
	export const BUN_OPTIONS: string;
	export const GIT_CONFIG_KEY_0: string;
	export const GIT_TERMINAL_PROMPT: string;
	export const AWS_ACCESS_KEY_ID: string;
	export const CLAUDE_CODE_SESSION_ID: string;
	export const GIT_CONFIG_KEY_1: string;
	export const _: string;
	export const NIX_SSL_CERT_FILE: string;
}

/**
 * This module provides access to environment variables that are injected _statically_ into your bundle at build time and are _publicly_ accessible.
 * 
 * |         | Runtime                                                                    | Build time                                                               |
 * | ------- | -------------------------------------------------------------------------- | ------------------------------------------------------------------------ |
 * | Private | [`$env/dynamic/private`](https://svelte.dev/docs/kit/$env-dynamic-private) | [`$env/static/private`](https://svelte.dev/docs/kit/$env-static-private) |
 * | Public  | [`$env/dynamic/public`](https://svelte.dev/docs/kit/$env-dynamic-public)   | [`$env/static/public`](https://svelte.dev/docs/kit/$env-static-public)   |
 * 
 * Static environment variables are [loaded by Vite](https://vitejs.dev/guide/env-and-mode.html#env-files) from `.env` files and `process.env` at build time and then statically injected into your bundle at build time, enabling optimisations like dead code elimination.
 * 
 * **_Public_ access:**
 * 
 * - This module _can_ be imported into client-side code
 * - **Only** variables that begin with [`config.kit.env.publicPrefix`](https://svelte.dev/docs/kit/configuration#env) (which defaults to `PUBLIC_`) are included
 * 
 * For example, given the following build time environment:
 * 
 * ```env
 * ENVIRONMENT=production
 * PUBLIC_BASE_URL=http://site.com
 * ```
 * 
 * With the default `publicPrefix` and `privatePrefix`:
 * 
 * ```ts
 * import { ENVIRONMENT, PUBLIC_BASE_URL } from '$env/static/public';
 * 
 * console.log(ENVIRONMENT); // => throws error during build
 * console.log(PUBLIC_BASE_URL); // => "http://site.com"
 * ```
 * 
 * The above values will be the same _even if_ different values for `ENVIRONMENT` or `PUBLIC_BASE_URL` are set at runtime, as they are statically replaced in your code with their build time values.
 */
declare module '$env/static/public' {
	
}

/**
 * This module provides access to environment variables set _dynamically_ at runtime and that are limited to _private_ access.
 * 
 * |         | Runtime                                                                    | Build time                                                               |
 * | ------- | -------------------------------------------------------------------------- | ------------------------------------------------------------------------ |
 * | Private | [`$env/dynamic/private`](https://svelte.dev/docs/kit/$env-dynamic-private) | [`$env/static/private`](https://svelte.dev/docs/kit/$env-static-private) |
 * | Public  | [`$env/dynamic/public`](https://svelte.dev/docs/kit/$env-dynamic-public)   | [`$env/static/public`](https://svelte.dev/docs/kit/$env-static-public)   |
 * 
 * Dynamic environment variables are defined by the platform you're running on. For example if you're using [`adapter-node`](https://github.com/sveltejs/kit/tree/main/packages/adapter-node) (or running [`vite preview`](https://svelte.dev/docs/kit/cli)), this is equivalent to `process.env`.
 * 
 * **_Private_ access:**
 * 
 * - This module cannot be imported into client-side code
 * - This module includes variables that _do not_ begin with [`config.kit.env.publicPrefix`](https://svelte.dev/docs/kit/configuration#env) _and do_ start with [`config.kit.env.privatePrefix`](https://svelte.dev/docs/kit/configuration#env) (if configured)
 * 
 * > [!NOTE] In `dev`, `$env/dynamic` includes environment variables from `.env`. In `prod`, this behavior will depend on your adapter.
 * 
 * > [!NOTE] To get correct types, environment variables referenced in your code should be declared (for example in an `.env` file), even if they don't have a value until the app is deployed:
 * >
 * > ```env
 * > MY_FEATURE_FLAG=
 * > ```
 * >
 * > You can override `.env` values from the command line like so:
 * >
 * > ```sh
 * > MY_FEATURE_FLAG="enabled" npm run dev
 * > ```
 * 
 * For example, given the following runtime environment:
 * 
 * ```env
 * ENVIRONMENT=production
 * PUBLIC_BASE_URL=http://site.com
 * ```
 * 
 * With the default `publicPrefix` and `privatePrefix`:
 * 
 * ```ts
 * import { env } from '$env/dynamic/private';
 * 
 * console.log(env.ENVIRONMENT); // => "production"
 * console.log(env.PUBLIC_BASE_URL); // => undefined
 * ```
 */
declare module '$env/dynamic/private' {
	export const env: {
		SVELTEKIT_FORK: string;
		NODE_ENV: string;
		INIT_CWD: string;
		CARGO_HTTP_CAINFO: string;
		ANT_IMAGE_REPOSITORY: string;
		npm_command: string;
		USE_SHTTP_MCP: string;
		ENV_MANAGER_ENABLE_DIAG_LOGS: string;
		IS_SANDBOX: string;
		npm_config_global_prefix: string;
		CLAUDE_CODE_EXECPATH: string;
		PWD: string;
		JAVA_HOME: string;
		npm_config_init_module: string;
		npm_config_globalconfig: string;
		CLOUDSDK_PROXY_PORT: string;
		CLOUDSDK_PROXY_ADDRESS: string;
		FSSPEC_GCS: string;
		https_proxy: string;
		CLAUDE_ADDITIONAL_DIRECTORIES: string;
		HOME: string;
		DOCUMENTS_MCP_SCRATCH_ROOT: string;
		HEX_CACERTS_PATH: string;
		CLAUDE_CODE_WEBSOCKET_AUTH_FILE_DESCRIPTOR: string;
		JAVA_TOOL_OPTIONS: string;
		npm_config_user_agent: string;
		PYTHONUNBUFFERED: string;
		CLAUDE_CODE_CONTAINER_ID: string;
		AI_AGENT: string;
		RUSTUP_HOME: string;
		npm_package_json: string;
		CLAUDE_CODE_TEE_SDK_STDOUT: string;
		no_proxy: string;
		CLAUDE_CODE_POST_FOR_SESSION_INGRESS_V2: string;
		CCR_SPAWN_TIMESTAMP_MS: string;
		CLAUDE_SESSION_INGRESS_TOKEN_FILE: string;
		OLDPWD: string;
		NO_PROXY: string;
		CLAUDE_CODE_REMOTE_SEND_KEEPALIVES: string;
		GIT_CONFIG_VALUE_2: string;
		npm_config_userconfig: string;
		CLOUDSDK_AUTH_ACCESS_TOKEN: string;
		RBENV_ROOT: string;
		UV_NATIVE_TLS: string;
		GRPC_DEFAULT_SSL_ROOTS_FILE_PATH: string;
		CCR_AGENT_PROXY_ENABLED: string;
		CLAUDE_CODE_USE_CCR_V2: string;
		GIT_EDITOR: string;
		GLOBAL_AGENT_HTTPS_PROXY: string;
		ANT_IMAGE_TAG: string;
		npm_config_https_proxy: string;
		AWS_CA_BUNDLE: string;
		CLAUDE_CODE_USER_EMAIL: string;
		NODE_EXTRA_CA_CERTS: string;
		GITHUB_TOKEN: string;
		CLAUDE_CODE_SYNC_SKILLS: string;
		CCR_EGRESS_GATEWAY_ENABLED: string;
		CLAUDE_ENABLE_STREAM_WATCHDOG: string;
		npm_lifecycle_event: string;
		NODE_OPTIONS: string;
		CLAUDE_CODE_BASE_REF: string;
		REQUESTS_CA_BUNDLE: string;
		CCR_ENABLE_TRACING: string;
		CLAUDE_CODE_DEBUG: string;
		npm_config_prefix: string;
		GCM_INTERACTIVE: string;
		COLOR: string;
		CLAUDE_CODE_ENVIRONMENT_RUNNER_VERSION: string;
		GIT_ASKPASS: string;
		CCR_SETTINGS_JSON_OVERLAY: string;
		CLAUDE_CODE_REMOTE_SESSION_ID: string;
		USE_BUILTIN_RIPGREP: string;
		CLAUDE_CODE_DIAGNOSTICS_FILE: string;
		BUN_INSTALL: string;
		DOCKER_HTTPS_PROXY: string;
		ANTHROPIC_BASE_URL: string;
		GH_TOKEN: string;
		SHLVL: string;
		EDITOR: string;
		CLOUDSDK_CORE_CUSTOM_CA_CERTS_FILE: string;
		GIT_SSL_CAINFO: string;
		CLAUDE_CODE_REMOTE: string;
		npm_config_npm_version: string;
		npm_config_cache: string;
		NODE: string;
		TERM: string;
		CLAUDE_CODE_ACCOUNT_UUID: string;
		SKIP_PLUGIN_MARKETPLACE: string;
		GIT_CONFIG_VALUE_0: string;
		MCP_TOOL_TIMEOUT: string;
		MCP_CONNECTION_NONBLOCKING: string;
		npm_config_node_gyp: string;
		SHELL: string;
		HTTPS_PROXY: string;
		PATH: string;
		DENO_TLS_CA_STORE: string;
		GIT_CONFIG_COUNT: string;
		CLAUDE_CODE_OAUTH_TOKEN_FILE_DESCRIPTOR: string;
		MAX_THINKING_TOKENS: string;
		GIT_CONFIG_VALUE_1: string;
		npm_config_local_prefix: string;
		npm_package_name: string;
		YARN_HTTPS_PROXY: string;
		CLAUDE_CODE_VERSION: string;
		GIT_CONFIG_KEY_2: string;
		COREPACK_ENABLE_AUTO_PIN: string;
		npm_config_noproxy: string;
		PLAYWRIGHT_BROWSERS_PATH: string;
		CCR_UPSTREAM_PROXY_ENABLED: string;
		npm_execpath: string;
		SSL_CERT_FILE: string;
		CLAUDE_AUTO_BACKGROUND_TASKS: string;
		CLAUDE_AFTER_LAST_COMPACT: string;
		CLAUDE_CODE_ORGANIZATION_UUID: string;
		CLOUDSDK_PROXY_TYPE: string;
		CLAUDE_CODE_ENTRYPOINT: string;
		ENVRUNNER_SKIP_ACK: string;
		CLAUDE_CODE_PROVIDER_MANAGED_BY_HOST: string;
		CLAUDE_CODE_PROXY_RESOLVES_HOSTS: string;
		CLAUDE_PID: string;
		NoDefaultCurrentDirectoryInExePath: string;
		CLAUDE_EFFORT: string;
		TRACEPARENT: string;
		CLAUDE_CODE_DISABLE_BUILTIN_ANTMCP: string;
		DENO_CERT: string;
		npm_package_version: string;
		CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD: string;
		CLAUDE_CODE_WORKER_EPOCH: string;
		HTTPLIB2_CA_CERTS: string;
		npm_node_execpath: string;
		DEBIAN_FRONTEND: string;
		CLAUDECODE: string;
		ELECTRON_GET_USE_PROXY: string;
		PIP_CERT: string;
		CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE: string;
		npm_lifecycle_script: string;
		CLAUDE_CODE_CHILD_SESSION: string;
		CLAUDE_AUTOCOMPACT_PCT_OVERRIDE: string;
		CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH: string;
		CCR_TEST_GITPROXY: string;
		AWS_SECRET_ACCESS_KEY: string;
		CURL_CA_BUNDLE: string;
		RUST_BACKTRACE: string;
		GLOBAL_AGENT_NO_PROXY: string;
		BUN_OPTIONS: string;
		GIT_CONFIG_KEY_0: string;
		GIT_TERMINAL_PROMPT: string;
		AWS_ACCESS_KEY_ID: string;
		CLAUDE_CODE_SESSION_ID: string;
		GIT_CONFIG_KEY_1: string;
		_: string;
		NIX_SSL_CERT_FILE: string;
		[key: `PUBLIC_${string}`]: undefined;
		[key: `${string}`]: string | undefined;
	}
}

/**
 * This module provides access to environment variables set _dynamically_ at runtime and that are _publicly_ accessible.
 * 
 * |         | Runtime                                                                    | Build time                                                               |
 * | ------- | -------------------------------------------------------------------------- | ------------------------------------------------------------------------ |
 * | Private | [`$env/dynamic/private`](https://svelte.dev/docs/kit/$env-dynamic-private) | [`$env/static/private`](https://svelte.dev/docs/kit/$env-static-private) |
 * | Public  | [`$env/dynamic/public`](https://svelte.dev/docs/kit/$env-dynamic-public)   | [`$env/static/public`](https://svelte.dev/docs/kit/$env-static-public)   |
 * 
 * Dynamic environment variables are defined by the platform you're running on. For example if you're using [`adapter-node`](https://github.com/sveltejs/kit/tree/main/packages/adapter-node) (or running [`vite preview`](https://svelte.dev/docs/kit/cli)), this is equivalent to `process.env`.
 * 
 * **_Public_ access:**
 * 
 * - This module _can_ be imported into client-side code
 * - **Only** variables that begin with [`config.kit.env.publicPrefix`](https://svelte.dev/docs/kit/configuration#env) (which defaults to `PUBLIC_`) are included
 * 
 * > [!NOTE] In `dev`, `$env/dynamic` includes environment variables from `.env`. In `prod`, this behavior will depend on your adapter.
 * 
 * > [!NOTE] To get correct types, environment variables referenced in your code should be declared (for example in an `.env` file), even if they don't have a value until the app is deployed:
 * >
 * > ```env
 * > MY_FEATURE_FLAG=
 * > ```
 * >
 * > You can override `.env` values from the command line like so:
 * >
 * > ```sh
 * > MY_FEATURE_FLAG="enabled" npm run dev
 * > ```
 * 
 * For example, given the following runtime environment:
 * 
 * ```env
 * ENVIRONMENT=production
 * PUBLIC_BASE_URL=http://example.com
 * ```
 * 
 * With the default `publicPrefix` and `privatePrefix`:
 * 
 * ```ts
 * import { env } from '$env/dynamic/public';
 * console.log(env.ENVIRONMENT); // => undefined, not public
 * console.log(env.PUBLIC_BASE_URL); // => "http://example.com"
 * ```
 * 
 * ```
 * 
 * ```
 */
declare module '$env/dynamic/public' {
	export const env: {
		[key: `PUBLIC_${string}`]: string | undefined;
	}
}
