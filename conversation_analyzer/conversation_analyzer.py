#!/usr/bin/env python3
"""
Conversation Analyzer

A command-line tool for analyzing conversation logs in JSON format.
Extracts statistics, identifies patterns, and highlights main discussion topics.

Useful for:
- Content summarization
- Communication pattern analysis
- Topic identification and tracking
- Conversation metrics and insights

Author: Built by Andrew using modern development practices including AI-assisted coding.
"""

import json
import sys
from datetime import datetime


def load_conversation_file(filepath):
    """
    Load a conversation JSON file and return the data in standardized format.
    Handles both formats:
    - New format: {"date": "...", "conversations": [...]}
    - Old format: [{...}, {...}] (direct array of conversations)
    
    Args:
        filepath: Path to the JSON file
        
    Returns:
        Dictionary containing the conversation data in standardized format
    """
    # Open the file and read it
    with open(filepath, 'r', encoding='utf-8') as file:
        raw_data = json.load(file)
    
    # Check if it's the new format (dict with 'conversations' key) or old format (direct list)
    if isinstance(raw_data, dict) and 'conversations' in raw_data:
        # New format - already structured correctly
        return raw_data
    elif isinstance(raw_data, list):
        # Old format - wrap it in the expected structure
        # Extract date from filename if possible, otherwise use "Unknown"
        import os
        filename = os.path.basename(filepath)
        # Try to extract date from filename like "daily_conversations_2025-10-25.json"
        date = "Unknown Date"
        if "20" in filename:  # Simple heuristic for year
            parts = filename.split('_')
            for part in parts:
                if part.startswith('20') and '.json' in part:
                    date = part.replace('.json', '')
                    break
        
        return {
            'date': date,
            'conversations': raw_data
        }
    else:
        raise ValueError("Unrecognized JSON format")


def detect_participants(data):
    """
    Detect participant names from the conversation data.
    
    Args:
        data: Dictionary from load_conversation_file()
        
    Returns:
        List of unique participant names (roles)
    """
    participants = set()
    
    for conversation in data['conversations']:
        for message in conversation['messages']:
            participants.add(message['role'])
    
    return sorted(list(participants))  # Sort for consistent ordering


def extract_topics(data, top_n=15):
    """
    Extract main topics from conversations using keyword frequency.
    
    Args:
        data: Dictionary from load_conversation_file()
        top_n: Number of top topics to return
        
    Returns:
        List of (word, count) tuples sorted by frequency
    """
    # Words to ignore (common words that don't indicate topics)
    stop_words = {
        'the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have', 'i',
        'it', 'for', 'not', 'on', 'with', 'he', 'as', 'you', 'do', 'at',
        'this', 'but', 'his', 'by', 'from', 'they', 'we', 'say', 'her', 'she',
        'or', 'an', 'will', 'my', 'one', 'all', 'would', 'there', 'their',
        'what', 'so', 'up', 'out', 'if', 'about', 'who', 'get', 'which', 'go',
        'me', 'when', 'make', 'can', 'like', 'time', 'no', 'just', 'him', 'know',
        'take', 'into', 'your', 'some', 'could', 'them', 'see', 'other', 'than',
        'then', 'now', 'look', 'only', 'come', 'its', 'over', 'think', 'also',
        'back', 'after', 'use', 'two', 'how', 'our', 'work', 'first', 'well',
        'way', 'even', 'new', 'want', 'because', 'any', 'these', 'give', 'day',
        'most', 'us', 'is', 'was', 'are', 'been', 'has', 'had', 'were', 'said',
        'did', 'having', 'may', 'am', 'are', 'im', 'youre', 'thats', 'dont',
        'ive', 'isnt', 'arent', 'wasnt', 'werent', 'wont', 'cant', 'couldnt'
    }
    
    # Dictionary to count word frequencies
    word_counts = {}
    
    # Loop through all conversations and messages
    for conversation in data['conversations']:
        for message in conversation['messages']:
            # Get the content (handle both string and nested structures)
            if isinstance(message['content'], str):
                content = message['content']
            else:
                content = str(message['content'])
            
            # Convert to lowercase and split into words
            words = content.lower().split()
            
            # Count each word
            for word in words:
                # Clean the word (remove punctuation)
                clean_word = ''.join(c for c in word if c.isalnum())
                
                # Skip if empty, too short, or a stop word
                if len(clean_word) < 3 or clean_word in stop_words:
                    continue
                
                # Count it
                if clean_word in word_counts:
                    word_counts[clean_word] += 1
                else:
                    word_counts[clean_word] = 1
    
    # Sort by frequency (most common first)
    sorted_topics = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)
    
    # Return top N
    return sorted_topics[:top_n]


def categorize_time_period(time_string):
    """
    Categorize a time string into a period of day.
    
    Args:
        time_string: String like "03:03 PM"
        
    Returns:
        String: "Morning", "Afternoon", "Evening", or "Night"
    """
    # Convert to datetime to get the hour
    time_obj = datetime.strptime(time_string, "%I:%M %p")
    hour = time_obj.hour  # 24-hour format (0-23)
    
    # Categorize based on hour
    if 6 <= hour < 12:
        return "Morning"
    elif 12 <= hour < 17:  # 17 = 5 PM
        return "Afternoon"
    elif 17 <= hour < 22:  # 22 = 10 PM
        return "Evening"
    else:
        return "Night"


def calculate_duration(start_time, end_time):
    """
    Calculate duration between two time strings.
    
    Args:
        start_time: String like "03:03 PM"
        end_time: String like "03:08 PM"
        
    Returns:
        Duration in minutes
    """
    # Convert time strings to datetime objects
    start = datetime.strptime(start_time, "%I:%M %p")
    end = datetime.strptime(end_time, "%I:%M %p")
    
    # Calculate difference
    duration = (end - start).total_seconds() / 60  # Convert to minutes
    return int(duration)


def get_basic_stats(data):
    """
    Calculate basic statistics from conversation data.
    
    Args:
        data: Dictionary from load_conversation_file()
        
    Returns:
        Dictionary with statistics
    """
    # Detect participants dynamically
    participants = detect_participants(data)
    
    stats = {
        'date': data['date'],
        'num_conversations': len(data['conversations']),
        'total_messages': 0,
        'participants': participants,
        'messages_by_participant': {p: 0 for p in participants},
        'conversation_lengths': [],
        'shortest_conversation': None,
        'longest_conversation': None,
        # Time period tracking
        'time_periods': {
            'Morning': 0,
            'Afternoon': 0,
            'Evening': 0,
            'Night': 0
        },
        # Conversation flow tracking
        'conversations_started_by': {p: 0 for p in participants},
        'message_lengths_by_participant': {p: [] for p in participants}
    }
    
    # Loop through each conversation
    for i, conversation in enumerate(data['conversations']):
        # Count messages in THIS conversation
        message_count = len(conversation['messages'])
        
        # Calculate time duration
        duration = calculate_duration(
            conversation['start_time'],
            conversation['end_time']
        )
        
        # Categorize the time period
        time_period = categorize_time_period(conversation['start_time'])
        stats['time_periods'][time_period] += message_count
        
        # Track who started this conversation (first message)
        first_speaker = conversation['messages'][0]['role']
        stats['conversations_started_by'][first_speaker] += 1
        
        # Store the length info
        conv_info = {
            'index': i + 1,
            'message_count': message_count,
            'duration_minutes': duration,
            'start_time': conversation['start_time'],
            'end_time': conversation['end_time'],
            'time_period': time_period
        }
        stats['conversation_lengths'].append(conv_info)
        
        # Track shortest and longest
        if stats['shortest_conversation'] is None or message_count < stats['shortest_conversation']['message_count']:
            stats['shortest_conversation'] = conv_info
        
        if stats['longest_conversation'] is None or message_count > stats['longest_conversation']['message_count']:
            stats['longest_conversation'] = conv_info
        
        # Loop through each message in the conversation
        for message in conversation['messages']:
            stats['total_messages'] += 1
            
            # Get message length (character count)
            if isinstance(message['content'], str):
                msg_length = len(message['content'])
            else:
                msg_length = len(str(message['content']))
            
            # Track by participant
            participant = message['role']
            stats['messages_by_participant'][participant] += 1
            stats['message_lengths_by_participant'][participant].append(msg_length)
    
    return stats


def print_stats(stats):
    """
    Print statistics in a nice readable format.
    
    Args:
        stats: Dictionary from get_basic_stats()
    """
    print(f"\n{'='*50}")
    print(f"Conversation Analysis for {stats['date']}")
    print(f"{'='*50}")
    print(f"\nTotal Conversations: {stats['num_conversations']}")
    print(f"Total Messages: {stats['total_messages']}")
    
    # Show messages per participant
    for participant in stats['participants']:
        count = stats['messages_by_participant'][participant]
        print(f"  - {participant}: {count}")
    
    # Show time period breakdown
    print(f"\n--- Time of Day Patterns ---")
    for period, count in stats['time_periods'].items():
        if stats['total_messages'] > 0:
            percentage = (count / stats['total_messages']) * 100
            print(f"{period:12} {count:3} messages ({percentage:5.1f}%)")
    
    # Show conversation flow
    print(f"\n--- Conversation Flow ---")
    print(f"\nConversations Started:")
    for participant in stats['participants']:
        count = stats['conversations_started_by'][participant]
        print(f"  - {participant}: {count}")
    
    # Show message length stats for each participant
    for participant in stats['participants']:
        lengths = stats['message_lengths_by_participant'][participant]
        if lengths:
            avg = sum(lengths) / len(lengths)
            longest = max(lengths)
            print(f"\n{participant}'s Messages:")
            print(f"  - Average length: {avg:.0f} characters")
            print(f"  - Longest message: {longest} characters")
    
    # Show conversation length info
    print(f"\n--- Conversation Lengths ---")
    print(f"\nShortest Conversation:")
    sc = stats['shortest_conversation']
    print(f"  Conversation #{sc['index']}: {sc['message_count']} messages, {sc['duration_minutes']} minutes")
    print(f"  ({sc['start_time']} - {sc['end_time']}) [{sc['time_period']}]")
    
    print(f"\nLongest Conversation:")
    lc = stats['longest_conversation']
    print(f"  Conversation #{lc['index']}: {lc['message_count']} messages, {lc['duration_minutes']} minutes")
    print(f"  ({lc['start_time']} - {lc['end_time']}) [{lc['time_period']}]")
    
    # Calculate average
    if stats['conversation_lengths']:
        total_messages_in_convs = sum(c['message_count'] for c in stats['conversation_lengths'])
        avg_messages = total_messages_in_convs / len(stats['conversation_lengths'])
        print(f"\nAverage messages per conversation: {avg_messages:.1f}")
    
    print(f"\n{'='*50}\n")


def main():
    """
    Main function - runs when you execute the script.
    """
    # Check if user provided a filename
    if len(sys.argv) < 2:
        print("\nUsage: python conversation_analyzer.py <filename>")
        print("Example: python conversation_analyzer.py daily_conversations_2025-10-30.json\n")
        sys.exit(1)
    
    filepath = sys.argv[1]
    
    # Check if file exists
    try:
        print(f"Loading conversation file: {filepath}...")
        data = load_conversation_file(filepath)
    except FileNotFoundError:
        print(f"\nError: File '{filepath}' not found!")
        print("Make sure the file exists in the current directory.\n")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"\nError: File '{filepath}' is not valid JSON!")
        print("Make sure it's a properly formatted JSON file.\n")
        sys.exit(1)
    
    print("Calculating statistics...")
    stats = get_basic_stats(data)
    
    print("Extracting topics...")
    topics = extract_topics(data)
    
    print_stats(stats)
    print_topics(topics)


def print_topics(topics):
    """
    Print extracted topics in a nice format.
    
    Args:
        topics: List of (word, count) tuples from extract_topics()
    """
    print(f"\n{'='*50}")
    print("Main Topics Discussed")
    print(f"{'='*50}\n")
    
    for i, (word, count) in enumerate(topics, 1):
        print(f"{i:2}. {word:20} ({count:3} mentions)")
    
    print(f"\n{'='*50}\n")


# This means "if you run this file directly, execute main()"
if __name__ == "__main__":
    main()