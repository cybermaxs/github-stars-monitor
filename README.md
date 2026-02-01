# Github Stars Monitor : Never miss a new top starred repository

This project is a _simple_ pipeline to get the top starred newly created repositories from Github.

![demo](./docs/demo.gif)

Internally, the project is built with :
* [dlt](https://dlthub.com/) as ingestion tool.
* [DuckDB](https://duckdb.org/) as database.
* [dbt](https://www.dbt.com/) as transformation tool.
* [Evidence](https://evidence.dev/) as dashboard.

The pipeline is scheduled to run every day at 12:00 AM UTC and deployed to [Github pages](https://cybermaxs.github.io/github-stars-monitor/).

## Development

### Prerequisites

The project requires:
* Python 3.13
* [uv](https://github.com/astral-sh/uv) for Python package management
* Node.js 18+ (only for the visualization part)
* A GitHub Personal Access Token (PAT) to fetch data from GitHub

### Setup

1. **Clone the repository**
```bash
git clone https://github.com/cybermaxs/github-stars-monitor.git
cd github-stars-monitor
```

2. **Create a GitHub Personal Access Token**
   - Go to GitHub Settings → Developer settings → Personal access tokens → [Tokens (classic)](https://github.com/settings/tokens)
   - Click "Generate new token (classic)"
   - Give it a descriptive name (e.g., "GitHub Stars Monitor")
   - Select scopes: `public_repo` (to read public repository data)
   - Click "Generate token" and copy the token

3. **Configure the token**

   Create a `.dlt/secrets.toml` file in the project root:
   ```bash
   mkdir -p .dlt
   cat > .dlt/secrets.toml << EOF
   [sources.github]
   access_token = "your_github_token_here"
   EOF
   ```

4. **Install dependencies**
```bash
make install
```

5. **Run the pipeline**
```bash
make run
```

### Configuration

You can customize the pipeline behavior using environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `GITHUB_LOOKBACK_DAYS` | How many days back to search for repositories | 60 |
| `GITHUB_MIN_STARS` | Minimum number of stars to include a repository | 500 |
| `GITHUB_RATE_LIMIT_THRESHOLD` | Stop pagination when rate limit falls below this | 500 |
| `LOG_LEVEL` | Logging level (DEBUG, INFO, WARNING, ERROR) | INFO |
| `EXTRACT_WORKERS` | Number of parallel workers for data extraction | 4 |

Example with custom configuration:
```bash
GITHUB_LOOKBACK_DAYS=30 GITHUB_MIN_STARS=1000 make run
```

### Available Commands

Common tasks are available in the `Makefile`:

```bash
make install    # Install all dependencies
make ingest     # Run data ingestion from GitHub API
make transform  # Run dbt transformations
make dashboard  # Build the Evidence dashboard
make run        # Run full pipeline (ingest + transform + dashboard)
make clean      # Remove the DuckDB database
make refresh    # Clean and run full pipeline
```

## Troubleshooting

### "GitHub access token is required but not provided"
Make sure you've created the `.dlt/secrets.toml` file with your GitHub token as described in the setup section.

### Rate limit errors
The pipeline automatically stops when the GitHub API rate limit gets low (default: 500 remaining calls). You can:
- Wait for the rate limit to reset (check the logs for reset time)
- Lower the `GITHUB_RATE_LIMIT_THRESHOLD` if you want to use more of your quota
- Use a different GitHub token with a fresh rate limit

### No data showing in dashboard
1. Check that the ingestion completed successfully: `ls -lh data/github.duckdb`
2. Verify transformations ran: `cd transform && uv run dbt test`
3. Check for errors in the logs

### DuckDB file is locked
If you see "database is locked" errors, make sure:
- No other process is accessing the database
- Close any open DuckDB connections
- Try `make clean` and `make run` to start fresh

## Feature Requests

If you have any feature requests, feel free to open an issue on the [GitHub repository](https://github.com/cybermaxs/github-stars-monitor/issues).

## Credits

This project is heavily inspired by [mdsinabox](https://github.com/matsonj/nba-monte-carlo) and [pypi-duck-flow](https://github.com/mehd-io/pypi-duck-flow).
