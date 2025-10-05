# Strava MCP server

[r-huijts/strava-mcp](https://github.com/r-huijts/strava-mcp) is a Model Context Protocol (MCP) server that connects to Strava API, providing tools to access Strava data through LLMs.

# Security Assessment

Claude Sonnet 4.5 says this code is ✅ Safe - No Major Concerns.

## Authentication & Data Handling

  - Uses standard OAuth 2.0 flow with Strava API (setup-auth.ts:107)
  - Tokens stored locally in .env file only (stravaClient.ts:317, 324-357)
  - All API calls go directly to Strava's official API (https://www.strava.com/api/v3) (stravaClient.ts:10)
  - No third-party data transmission - your data stays between your machine and Strava

### Access Scopes

  - Requests: profile:read_all, activity:read_all, activity:read, profile:write (setup-auth.ts:10)
  - profile:write only enables starring/unstarring segments (stravaClient.ts:867-905)
  - No ability to delete activities or modify workout data

##  Code Quality

  - Uses Zod for input validation (stravaClient.ts:31-42)
  - Proper error handling with token refresh (stravaClient.ts:359-401)
  - Read-only operations except segment starring
  - File exports limited to configured ROUTE_EXPORT_PATH directory

##  Token Security

  - Automatic token refresh implementation is correct (stravaClient.ts:363-401)
  - Tokens updated in both memory and .env file (stravaClient.ts:389-393)
  - No token logging or external transmission

##  Minor Recommendations

  1. `.env` file permissions: After setup, ensure .env has restricted permissions:
    chmod 600 .env
  2. Optional: Review scopes: If you don't plan to star segments, you could request without profile:write scope (though this is very low risk)

##  Verdict: SAFE TO USE

This is a legitimate, well-structured MCP server that securely connects to Strava. Your data remains private between your machine and Strava's servers. The code follows security best practices and has no malicious patterns.
