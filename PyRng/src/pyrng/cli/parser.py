"""Command-line argument parsing."""

import argparse
from pathlib import Path
from typing import List, Optional
import sys

from pyrng import __version__


def create_parser() -> argparse.ArgumentParser:
    """Create and configure the argument parser.
    
    Returns:
        Configured ArgumentParser instance with all CLI options.
    
    Examples:
        >>> parser = create_parser()
        >>> args = parser.parse_args(["uniform", "-n", "10"])
        >>> args.distribution
        'uniform'
        >>> args.count
        10
    """
    parser = argparse.ArgumentParser(
        prog="pyrng",
        description="Flexible random number generator with multiple distributions",
        epilog="Examples:\n"
               "  pyrng uniform -n 100 --low 0 --high 10\n"
               "  pyrng normal -n 1000 --mu 0 --sigma 1 -o output.csv -f csv\n"
               "  pyrng exponential -n 500 --lambda 1.5 -s 42",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    # Global options
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}"
    )
    parser.add_argument(
        "-i", "--interactive",
        action="store_true",
        help="start interactive mode"
    )
    parser.add_argument(
        "-c", "--config",
        type=Path,
        help="path to configuration file"
    )
    parser.add_argument(
        "--create-config",
        action="store_true",
        help="create default configuration file and exit"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="enable verbose logging"
    )
    parser.add_argument(
        "-s", "--seed",
        type=int,
        help="random seed for reproducibility"
    )
    parser.add_argument(
        "-o", "--output",
        type=Path,
        help="output file path (default: stdout)"
    )
    parser.add_argument(
        "-f", "--format",
        choices=["text", "csv", "json", "binary"],
        default="text",
        help="output format (default: text)"
    )
    
    # Subcommands for different distributions
    # Not required if using interactive mode or creating config
    subparsers = parser.add_subparsers(
        dest="distribution",
        required=False,
        help="probability distribution to use"
    )
    
    # Uniform distribution
    uniform_parser = subparsers.add_parser(
        "uniform",
        help="uniform distribution U(low, high)"
    )
    uniform_parser.add_argument(
        "-n", "--count",
        type=int,
        required=True,
        help="number of samples to generate"
    )
    uniform_parser.add_argument(
        "--low",
        type=float,
        default=0.0,
        help="lower bound (inclusive, default: 0.0)"
    )
    uniform_parser.add_argument(
        "--high",
        type=float,
        default=1.0,
        help="upper bound (exclusive, default: 1.0)"
    )
    
    # Normal distribution
    normal_parser = subparsers.add_parser(
        "normal",
        help="normal (Gaussian) distribution N(mu, sigma²)"
    )
    normal_parser.add_argument(
        "-n", "--count",
        type=int,
        required=True,
        help="number of samples to generate"
    )
    normal_parser.add_argument(
        "--mu",
        type=float,
        default=0.0,
        help="mean (default: 0.0)"
    )
    normal_parser.add_argument(
        "--sigma",
        type=float,
        default=1.0,
        help="standard deviation (default: 1.0)"
    )
    
    # Exponential distribution
    exponential_parser = subparsers.add_parser(
        "exponential",
        help="exponential distribution Exp(lambda)"
    )
    exponential_parser.add_argument(
        "-n", "--count",
        type=int,
        required=True,
        help="number of samples to generate"
    )
    exponential_parser.add_argument(
        "--lambda",
        dest="lam",
        type=float,
        default=1.0,
        help="rate parameter (default: 1.0)"
    )
    
    # Binomial distribution
    binomial_parser = subparsers.add_parser(
        "binomial",
        help="binomial distribution B(n, p)"
    )
    binomial_parser.add_argument(
        "-n", "--count",
        type=int,
        required=True,
        help="number of samples to generate"
    )
    binomial_parser.add_argument(
        "--trials",
        type=int,
        default=10,
        help="number of trials (default: 10)"
    )
    binomial_parser.add_argument(
        "--p",
        type=float,
        default=0.5,
        help="probability of success (default: 0.5)"
    )
    
    # Poisson distribution
    poisson_parser = subparsers.add_parser(
        "poisson",
        help="Poisson distribution Pois(lambda)"
    )
    poisson_parser.add_argument(
        "-n", "--count",
        type=int,
        required=True,
        help="number of samples to generate"
    )
    poisson_parser.add_argument(
        "--lambda",
        dest="lam",
        type=float,
        default=1.0,
        help="rate parameter (default: 1.0)"
    )
    
    return parser


def parse_args(args: Optional[List[str]] = None) -> argparse.Namespace:
    """Parse command-line arguments.
    
    Args:
        args: List of arguments to parse. If None, uses sys.argv.
    
    Returns:
        Parsed arguments as Namespace.
    
    Examples:
        >>> args = parse_args(["uniform", "-n", "10"])
        >>> args.distribution
        'uniform'
    """
    parser = create_parser()
    return parser.parse_args(args)
