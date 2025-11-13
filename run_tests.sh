#!/usr/bin/env bash
#
# Test runner script for haveibeenpwned library
#

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Have I Been Pwned Test Suite${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Check if pytest is installed
if ! command -v pytest &> /dev/null; then
    echo -e "${RED}Error: pytest is not installed${NC}"
    echo "Install test dependencies with: pip install -r requirements-test.txt"
    exit 1
fi

# Function to run tests
run_tests() {
    local mode=$1
    local markers=$2
    local description=$3
    
    echo -e "${YELLOW}Running ${description}...${NC}"
    echo ""
    
    if [ -n "$markers" ]; then
        pytest -m "$markers" "$@"
    else
        pytest "$@"
    fi
    
    local exit_code=$?
    echo ""
    
    if [ $exit_code -eq 0 ]; then
        echo -e "${GREEN}✓ ${description} passed${NC}"
    else
        echo -e "${RED}✗ ${description} failed${NC}"
        return $exit_code
    fi
    
    echo ""
    return 0
}

# Parse command line arguments
MODE=${1:-all}

case $MODE in
    mock|unit)
        echo -e "${BLUE}Running unit tests with mocked API...${NC}"
        echo ""
        run_tests "mock" "unit" "Unit Tests (Mocked)"
        ;;
    
    live|integration)
        echo -e "${BLUE}Running integration tests with live API...${NC}"
        echo -e "${YELLOW}Note: Set HIBP_API_KEY environment variable for full testing${NC}"
        echo ""
        run_tests "live" "integration" "Integration Tests (Live API)"
        ;;
    
    coverage|cov)
        echo -e "${BLUE}Running all tests with coverage...${NC}"
        echo ""
        pytest --cov=haveibeenpwned \
               --cov-report=html \
               --cov-report=term-missing \
               --cov-report=xml \
               -v
        
        echo ""
        echo -e "${GREEN}✓ Coverage report generated${NC}"
        echo "  - HTML: htmlcov/index.html"
        echo "  - XML: coverage.xml"
        ;;
    
    quick)
        echo -e "${BLUE}Running quick tests (unit only, no coverage)...${NC}"
        echo ""
        pytest -m unit -v --tb=short
        ;;
    
    all)
        echo -e "${BLUE}Running all tests...${NC}"
        echo ""
        
        # Run unit tests first
        run_tests "all-unit" "unit" "Unit Tests (Mocked)" || exit 1
        
        # Run integration tests
        if [ -n "$HIBP_API_KEY" ]; then
            run_tests "all-integration" "integration" "Integration Tests (Live API)" || exit 1
        else
            echo -e "${YELLOW}⚠ Skipping integration tests (no HIBP_API_KEY set)${NC}"
            echo ""
        fi
        
        echo -e "${GREEN}========================================${NC}"
        echo -e "${GREEN}All tests completed successfully!${NC}"
        echo -e "${GREEN}========================================${NC}"
        ;;
    
    help|--help|-h)
        echo "Usage: $0 [MODE]"
        echo ""
        echo "Modes:"
        echo "  mock, unit       - Run unit tests with mocked API"
        echo "  live, integration - Run integration tests with live API"
        echo "  coverage, cov    - Run all tests with coverage report"
        echo "  quick            - Run quick unit tests only"
        echo "  all              - Run all tests (default)"
        echo "  help             - Show this help message"
        echo ""
        echo "Examples:"
        echo "  $0                  # Run all tests"
        echo "  $0 mock             # Run unit tests only"
        echo "  $0 live             # Run integration tests"
        echo "  $0 coverage         # Generate coverage report"
        echo ""
        echo "Environment Variables:"
        echo "  HIBP_API_KEY      - API key for live integration tests"
        echo ""
        exit 0
        ;;
    
    *)
        echo -e "${RED}Error: Unknown mode '$MODE'${NC}"
        echo "Run '$0 help' for usage information"
        exit 1
        ;;
esac

exit 0
