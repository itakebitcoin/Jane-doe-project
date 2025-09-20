# Jane Doe Search System

**Created by:** [@itakebitcoin](https://github.com/itakebitcoin)  
**Repository:** [Jane-Doe-Project](https://github.com/itakebitcoin/Jane-Doe-Project)

A Python-based system for searching Jane Doe databases to help reunite families with missing loved ones. This tool provides both command-line and (planned) graphical interfaces for searching unidentified persons databases using physical characteristics and location filters.

## 🎯 Purpose

This system is designed to help families find missing loved ones by searching publicly available Jane Doe databases. It uses advanced matching algorithms to compare physical characteristics and location data across multiple databases.

## ⚠️ Important Notice

**This tool is intended for ethical use only.** Please use it responsibly to help reunite families with missing loved ones. Always work with law enforcement for verification of any potential matches.

## 🌟 Features

- **Multi-Database Search**: Searches NamUs, DoeNetwork, and other public databases
- **Physical Characteristics Matching**: Height, weight, race, sex, age, distinguishing marks
- **Location Filtering**: State, county, city-based searches
- **Fuzzy Matching**: Advanced algorithms for approximate matches
- **Confidence Scoring**: Results ranked by match probability
- **Multiple Interfaces**: Command-line interface (GUI planned)
- **Ethical Guidelines**: Built-in reminders for responsible usage

## 📋 Requirements

- Python 3.7 or higher
- Internet connection for database access
- Windows, macOS, or Linux

## 🚀 Installation

1. **Clone or download this repository**
```bash
git clone https://github.com/itakebitcoin/Jane-Doe-Project
cd Jane-Doe-Project
```

2. **Install Python dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the system**
```bash
python main.py
```

## 🖥️ Usage

### Command Line Interface

Start the interactive CLI:
```bash
python main.py
```

The CLI provides these options:
1. **Set Physical Characteristics** - Enter height, weight, race, sex, age, distinguishing marks
2. **Set Location Filters** - Specify state, county, city
3. **Perform Search** - Search databases with current criteria
4. **Show Current Criteria** - Review your search parameters
5. **Clear Criteria** - Reset all search parameters
6. **Help & Instructions** - Detailed usage guide
7. **Ethics & Guidelines** - Important ethical usage information

### Example Search Process

1. Start the program: `python main.py`
2. Choose option 1 to set physical characteristics
3. Enter known details (height: 5'6", weight: 140 lbs, etc.)
4. Choose option 2 to set location (if known)
5. Choose option 3 to perform the search
6. Review results ranked by confidence score

## 📊 Understanding Results

Results are displayed with:
- **Confidence Score**: Percentage indicating match likelihood
- **Case Information**: Database source, case ID, URL
- **Physical Details**: Height, weight, race, sex, age
- **Location**: Where remains were found
- **Match Reasons**: Why this case was considered a match

### Confidence Levels
- **HIGH (80%+)**: Strong potential match
- **MEDIUM (60-79%)**: Good potential match  
- **LOW (40-59%)**: Possible match worth investigating
- **VERY LOW (<40%)**: Weak match, review carefully

## 🗃️ Supported Databases

### Currently Implemented
- **NamUs** (National Missing and Unidentified Persons System)
- **DoeNetwork** (Volunteer-run database)

### Planned Additions
- Local coroner office databases
- State-specific databases
- International databases (future)

## 🔧 Configuration

### Search Sensitivity
You can adjust the minimum confidence threshold by modifying the `SearchEngine` settings in the code.

### Database Selection
Choose which databases to search through the CLI or by modifying the `SearchCriteria`.

## 📁 Project Structure

```
Jane-Doe-Project/
├── main.py                 # Main entry point
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── .github/
│   └── copilot-instructions.md
└── src/
    ├── models/            # Data models
    │   ├── __init__.py
    │   └── person.py      # PersonRecord, SearchCriteria
    ├── database/          # Database interfaces
    │   ├── __init__.py
    │   ├── base.py        # Abstract interface
    │   ├── namus.py       # NamUs interface
    │   ├── doenetwork.py  # DoeNetwork interface
    │   └── manager.py     # Database coordinator
    ├── search/            # Search engine
    │   ├── __init__.py
    │   ├── matching.py    # Fuzzy matching algorithms
    │   └── engine.py      # Search coordinator
    ├── cli/               # Command-line interface
    │   ├── __init__.py
    │   └── interface.py   # CLI implementation
    └── utils/             # Utilities
        ├── __init__.py
        └── validation.py  # Input validation
```

## 🤝 Contributing

This project welcomes contributions that improve its ability to help families find missing loved ones. Please ensure all contributions maintain the ethical focus of the project.

### Development Setup
1. Fork the repository at [https://github.com/itakebitcoin/Jane-Doe-Project](https://github.com/itakebitcoin/Jane-Doe-Project)
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📜 Ethical Guidelines

### DO:
- Use this tool to help find missing family members
- Contact law enforcement with potential matches
- Respect the privacy and dignity of the deceased
- Be patient and thorough in your search
- Follow up responsibly on promising leads

### DON'T:
- Use this for curiosity or entertainment
- Share sensitive information publicly
- Make assumptions based on limited information
- Contact families directly without law enforcement
- Use for any commercial purposes

## ⚖️ Legal Considerations

- This tool accesses only publicly available information
- Users are responsible for ethical and legal use
- No guarantees are made about data accuracy
- Always verify information through proper authorities

## 🐛 Troubleshooting

### Common Issues

**"No results found"**
- Try broader search criteria (wider height/weight ranges)
- Check if databases are accessible
- Verify search parameters are reasonable

**"Connection errors"**
- Check internet connection
- Some databases may have temporary outages
- Try again later

**"Import errors"**
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Check Python version (3.7+ required)

### Getting Help

1. Check this README for common solutions
2. Review the CLI help system (option 6)
3. Verify your search criteria are reasonable
4. Check database availability

## 📞 Support

This is a tool designed to help families in their time of need. If you're using this system to search for a missing loved one, please also:

- Contact local law enforcement
- File missing person reports if not already done
- Consider reaching out to victim advocacy groups
- Connect with support services for families of missing persons

## 🔮 Future Enhancements

- Graphical user interface (GUI)
- Additional database integrations
- Photo comparison capabilities
- Advanced filtering options
- Mobile app version
- API for integration with other tools

## 📝 Version History

- **v1.0.0** - Initial release with CLI interface and basic database support

---

**Remember**: This tool provides leads, not definitive identifications. Always work with proper authorities for verification and never lose hope in your search for missing loved ones.
