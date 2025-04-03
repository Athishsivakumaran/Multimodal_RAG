import time
import logging
import re
from base64 import b64decode

MAX_RETRIES = 5  # Maximum number of retries
DEFAULT_WAIT_TIME = 30  # Default wait time before retrying
MIN_CONCURRENCY = 1  # Minimum concurrency (to prevent overloading)
MAX_CONCURRENCY = 3  # Maximum concurrency (adjust as needed)



def extract_wait_time(error_message):
    """Extracts the suggested wait time from the API response."""
    match = re.search(r"Please try again in ([\d\.]+)s", error_message)
    return float(match.group(1)) if match else DEFAULT_WAIT_TIME



def retry_with_adaptive_checkpoint(func, data_chunks, batch_params):
    """Retries with adaptive rate limiting and progress tracking."""
    completed = []  # Store successfully processed summaries
    remaining = data_chunks[:]  # Copy to avoid modifying the original list
    concurrency = batch_params.get("max_concurrency", MAX_CONCURRENCY)  # Start with max concurrency

    for attempt in range(MAX_RETRIES):
        try:
            while remaining:
                logging.info(f"Processing {len(remaining)} remaining chunks with concurrency {concurrency}...")

                # Process batch with current concurrency
                batch = remaining[:concurrency]
                summaries = func(batch, {"max_concurrency": concurrency})

                # Move processed chunks from remaining to completed
                completed.extend(summaries)
                remaining = remaining[len(batch):]

                logging.info(f"Successfully processed {len(completed)} chunks.")

            return completed  # Return completed results

        except Exception as e:
            error_str = str(e)
            if "rate_limit_exceeded" in error_str or "Rate limit reached" in error_str:
                wait_time = extract_wait_time(error_str)  # Extract dynamic wait time
                concurrency = max(MIN_CONCURRENCY, concurrency - 1)  # Reduce concurrency
                logging.warning(f"Rate limit hit. Reducing concurrency to {concurrency}. Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                raise  # Raise unexpected errors

    logging.error("Max retries reached. Some chunks may be missing.")
    return completed  # Return whatever was completed before failure




def parse_docs(docs):
    """Split base64-encoded images and texts"""
    b64 = []
    text = []
    for doc in docs:
        try:
            b64decode(doc)
            b64.append(doc)
        except Exception as e:
            text.append({"text":doc})
    return {"images": b64, "texts": text}



