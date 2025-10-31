# Conversation Analyzer

A Python command-line tool for analyzing conversation logs stored in JSON format. Extracts meaningful statistics, identifies communication patterns, and highlights main discussion topics.

## Features

- **Message Statistics**: Track total messages, conversation counts, and message distribution between participants
- **Time Pattern Analysis**: Identify when conversations happen most (Morning/Afternoon/Evening/Night)
- **Conversation Flow**: Analyze who initiates conversations and average message lengths
- **Topic Extraction**: Automatically identify the most frequently discussed topics using keyword analysis
- **Conversation Metrics**: Find longest/shortest conversations, average conversation length, and duration tracking

## Requirements

- Python 3.6 or higher
- No external dependencies (uses only Python standard library)

## Installation

1. Clone this repository or download `conversation_analyzer.py`
2. Make sure you have Python 3 installed
3. No additional installation needed!

## Usage

```bash
python conversation_analyzer.py <path_to_json_file>
```

### Example

```bash
python conversation_analyzer.py daily_conversations_2025-10-30.json
```

## JSON Format

The tool expects conversation logs in the following JSON format:

```json
{
  "date": "YYYY-MM-DD",
  "conversations": [
    {
      "start_time": "HH:MM AM/PM",
      "end_time": "HH:MM AM/PM",
      "messages": [
        {
          "role": "Person1",
          "content": "Message text here"
        },
        {
          "role": "Person2",
          "content": "Response text here"
        }
      ]
    }
  ]
}
```

## Output Example

```
==================================================
Conversation Analysis for 2025-10-30
==================================================

Total Conversations: 14
Total Messages: 596
  - Person1: 303
  - Person2: 293

--- Time of Day Patterns ---
Morning        0 messages (  0.0%)
Afternoon     71 messages ( 11.9%)
Evening      525 messages ( 88.1%)
Night          0 messages (  0.0%)

--- Conversation Flow ---
Conversations Started:
  - Person1: 14
  - Person2: 0

Person1's Messages:
  - Average length: 3869 characters
  - Longest message: 105331 characters

Person2's Messages:
  - Average length: 1538 characters
  - Longest message: 7785 characters

--- Main Topics Discussed ---
1. project             (245 mentions)
2. analysis            (189 mentions)
3. conversation        (167 mentions)
...
```

## How It Works

### Topic Extraction
The tool uses keyword frequency analysis to identify main topics:
1. Extracts all words from conversation content
2. Filters out common "stop words" (the, and, is, etc.)
3. Counts word frequency
4. Returns the most frequently mentioned terms

### Time Categorization
Conversations are categorized by start time:
- **Morning**: 6 AM - 12 PM
- **Afternoon**: 12 PM - 5 PM
- **Evening**: 5 PM - 10 PM
- **Night**: 10 PM - 6 AM

## Use Cases

- **Personal Analytics**: Track your communication patterns over time
- **Content Research**: Identify trending topics in conversations
- **Data Analysis**: Extract insights from conversation datasets
- **Summarization Aid**: Get quick overviews of lengthy conversation logs

## Future Enhancements

Potential features for future versions:
- Support for multiple file formats (CSV, TXT)
- Sentiment analysis
- Conversation visualization (charts/graphs)
- Export results to various formats
- Multi-day analysis and trend tracking

## Contributing

Feel free to fork this project and submit pull requests with improvements!

## License

MIT License - Feel free to use and modify as needed.

## Author

Built by Andrew using modern development practices including AI-assisted coding.
