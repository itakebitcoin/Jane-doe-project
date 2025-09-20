import os
import sys
from typing import Optional, List
from colorama import init, Fore, Back, Style

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ..models import SearchCriteria, PhysicalCharacteristics, Location, Race, Sex
from ..search import SearchEngine


class CLIInterface:
    """Command-line interface for the Jane Doe search system"""
    
    def __init__(self):
        init()  # Initialize colorama for Windows
        self.search_engine = SearchEngine()
        self.criteria = SearchCriteria()
        
    def run(self):
        """Main CLI loop"""
        self.show_welcome()
        
        while True:
            try:
                self.show_main_menu()
                choice = input(f"{Fore.CYAN}Enter your choice: {Style.RESET_ALL}").strip()
                
                if choice == '1':
                    self.set_physical_characteristics()
                elif choice == '2':
                    self.set_location_filters()
                elif choice == '3':
                    self.perform_search()
                elif choice == '4':
                    self.show_current_criteria()
                elif choice == '5':
                    self.clear_criteria()
                elif choice == '6':
                    self.show_help()
                elif choice == '7':
                    self.show_ethics()
                elif choice == '0' or choice.lower() == 'quit':
                    self.show_goodbye()
                    break
                else:
                    print(f"{Fore.RED}Invalid choice. Please try again.{Style.RESET_ALL}")
                    
            except KeyboardInterrupt:
                print(f"\n{Fore.YELLOW}Operation cancelled.{Style.RESET_ALL}")
            except Exception as e:
                print(f"{Fore.RED}An error occurred: {e}{Style.RESET_ALL}")
    
    def show_welcome(self):
        """Show welcome message"""
        print(f"\n{Fore.BLUE}{'='*60}")
        print(f"{Fore.BLUE}        JANE DOE DATABASE SEARCH SYSTEM")
        print(f"{Fore.BLUE}        Helping Reunite Families")
        print(f"{Fore.BLUE}{'='*60}{Style.RESET_ALL}")
        print(f"\n{Fore.YELLOW}This system searches publicly available Jane Doe databases")
        print(f"to help identify unidentified persons and reunite families.{Style.RESET_ALL}")
        print(f"\n{Fore.RED}IMPORTANT: Please use this tool ethically and responsibly.{Style.RESET_ALL}")
    
    def show_main_menu(self):
        """Show main menu options"""
        print(f"\n{Fore.GREEN}{'='*40}")
        print(f"{Fore.GREEN}           MAIN MENU")
        print(f"{Fore.GREEN}{'='*40}{Style.RESET_ALL}")
        print(f"1. Set Physical Characteristics")
        print(f"2. Set Location Filters")
        print(f"3. {Fore.YELLOW}Perform Search{Style.RESET_ALL}")
        print(f"4. Show Current Search Criteria")
        print(f"5. Clear All Criteria")
        print(f"6. Help & Instructions")
        print(f"7. Ethics & Guidelines")
        print(f"0. Quit")
        print(f"{Fore.GREEN}{'='*40}{Style.RESET_ALL}")
    
    def set_physical_characteristics(self):
        """Set physical characteristics for search"""
        print(f"\n{Fore.GREEN}Physical Characteristics{Style.RESET_ALL}")
        print("Enter the known physical characteristics. Press Enter to skip any field.")
        
        # Height
        print(f"\n{Fore.CYAN}Height:{Style.RESET_ALL}")
        height_min = self.get_height_input("Minimum height (e.g., 5'6\" or 66 inches): ")
        height_max = self.get_height_input("Maximum height (e.g., 5'10\" or 70 inches): ")
        
        if height_min:
            self.criteria.physical_characteristics.height_min = height_min
        if height_max:
            self.criteria.physical_characteristics.height_max = height_max
        
        # Weight
        print(f"\n{Fore.CYAN}Weight:{Style.RESET_ALL}")
        weight_min = self.get_integer_input("Minimum weight (lbs): ")
        weight_max = self.get_integer_input("Maximum weight (lbs): ")
        
        if weight_min:
            self.criteria.physical_characteristics.weight_min = weight_min
        if weight_max:
            self.criteria.physical_characteristics.weight_max = weight_max
        
        # Sex
        print(f"\n{Fore.CYAN}Sex:{Style.RESET_ALL}")
        self.show_sex_options()
        sex_choice = input("Enter choice (1-3): ").strip()
        if sex_choice == '1':
            self.criteria.physical_characteristics.sex = Sex.MALE
        elif sex_choice == '2':
            self.criteria.physical_characteristics.sex = Sex.FEMALE
        elif sex_choice == '3':
            self.criteria.physical_characteristics.sex = Sex.UNKNOWN
        
        # Race
        print(f"\n{Fore.CYAN}Race/Ethnicity:{Style.RESET_ALL}")
        self.show_race_options()
        race_choice = input("Enter choice (1-8): ").strip()
        race_map = {
            '1': Race.WHITE,
            '2': Race.BLACK_AFRICAN_AMERICAN,
            '3': Race.HISPANIC_LATINO,
            '4': Race.ASIAN,
            '5': Race.NATIVE_AMERICAN,
            '6': Race.PACIFIC_ISLANDER,
            '7': Race.MULTIRACIAL,
            '8': Race.UNKNOWN
        }
        if race_choice in race_map:
            self.criteria.physical_characteristics.race = race_map[race_choice]
        
        # Age
        print(f"\n{Fore.CYAN}Age:{Style.RESET_ALL}")
        age_min = self.get_integer_input("Minimum age: ")
        age_max = self.get_integer_input("Maximum age: ")
        
        if age_min:
            self.criteria.physical_characteristics.age_min = age_min
        if age_max:
            self.criteria.physical_characteristics.age_max = age_max
        
        # Distinguishing marks
        print(f"\n{Fore.CYAN}Distinguishing Marks:{Style.RESET_ALL}")
        print("Enter any distinguishing marks (tattoos, scars, birthmarks, etc.)")
        print("Enter one per line. Press Enter twice when done.")
        
        marks = []
        while True:
            mark = input("Mark: ").strip()
            if not mark:
                break
            marks.append(mark)
        
        if marks:
            self.criteria.physical_characteristics.distinguishing_marks = marks
        
        print(f"{Fore.GREEN}Physical characteristics updated!{Style.RESET_ALL}")
    
    def set_location_filters(self):
        """Set location filters for search"""
        print(f"\n{Fore.GREEN}Location Filters{Style.RESET_ALL}")
        print("Enter location information to narrow your search.")
        
        # State
        state = input(f"{Fore.CYAN}State (e.g., CA, TX, NY): {Style.RESET_ALL}").strip().upper()
        if state:
            self.criteria.location.state = state
        
        # County
        county = input(f"{Fore.CYAN}County: {Style.RESET_ALL}").strip()
        if county:
            self.criteria.location.county = county
        
        # City
        city = input(f"{Fore.CYAN}City: {Style.RESET_ALL}").strip()
        if city:
            self.criteria.location.city = city
        
        print(f"{Fore.GREEN}Location filters updated!{Style.RESET_ALL}")
    
    def perform_search(self):
        """Perform search with current criteria"""
        if not self.has_search_criteria():
            print(f"{Fore.RED}No search criteria set. Please set some criteria first.{Style.RESET_ALL}")
            return
        
        print(f"\n{Fore.YELLOW}Searching databases...{Style.RESET_ALL}")
        print("This may take a moment...")
        
        # Show what we're searching for
        print(f"\n{Fore.CYAN}Search Summary:{Style.RESET_ALL}")
        self.show_search_summary()
        
        try:
            # Check available databases
            available_dbs = self.search_engine.get_available_databases()
            print(f"\n{Fore.CYAN}Available databases: {', '.join(available_dbs)}{Style.RESET_ALL}")
            
            results = self.search_engine.search(self.criteria)
            print(f"\n{Fore.CYAN}Search completed. Found {len(results)} potential matches.{Style.RESET_ALL}")
            self.display_results(results)
        except Exception as e:
            print(f"{Fore.RED}Search failed: {e}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}This may be due to database connectivity issues.{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Try adjusting your search criteria or check your internet connection.{Style.RESET_ALL}")
    
    def show_search_summary(self):
        """Show a brief summary of search criteria"""
        pc = self.criteria.physical_characteristics
        loc = self.criteria.location
        
        summary = []
        
        if pc.sex:
            summary.append(f"Sex: {pc.sex.value}")
        if pc.race:
            summary.append(f"Race: {pc.race.value}")
        if pc.height_min or pc.height_max:
            height = self.format_height(pc.height_min, pc.height_max)
            summary.append(f"Height: {height}")
        if pc.weight_min or pc.weight_max:
            weight = self.format_weight(pc.weight_min, pc.weight_max)
            summary.append(f"Weight: {weight}")
        if pc.age_min or pc.age_max:
            age = self.format_age(pc.age_min, pc.age_max)
            summary.append(f"Age: {age}")
        if loc.state:
            summary.append(f"State: {loc.state}")
        if loc.county:
            summary.append(f"County: {loc.county}")
        if loc.city:
            summary.append(f"City: {loc.city}")
        
        if summary:
            print("  " + " | ".join(summary))
        else:
            print("  No specific criteria set (broad search)")
    
    def display_results(self, results):
        """Display search results"""
        if not results:
            print(f"\n{Fore.YELLOW}No matches found.{Style.RESET_ALL}")
            print("Try adjusting your search criteria or expanding the ranges.")
            return
        
        print(f"\n{Fore.GREEN}Found {len(results)} potential matches:{Style.RESET_ALL}")
        print(f"{Fore.GREEN}{'='*60}{Style.RESET_ALL}")
        
        for i, result in enumerate(results[:10], 1):  # Show top 10 results
            record = result.person_record
            confidence = result.confidence_score
            
            print(f"\n{Fore.CYAN}Match #{i} - Confidence: {confidence:.1%}{Style.RESET_ALL}")
            print(f"Database: {record.database_source}")
            print(f"Case ID: {record.case_id}")
            
            if record.case_url:
                print(f"URL: {record.case_url}")
            
            # Physical characteristics
            pc = record.physical_characteristics
            if pc.height_min or pc.height_max:
                height = self.format_height(pc.height_min, pc.height_max)
                print(f"Height: {height}")
            
            if pc.weight_min or pc.weight_max:
                weight = self.format_weight(pc.weight_min, pc.weight_max)
                print(f"Weight: {weight}")
            
            if pc.sex:
                print(f"Sex: {pc.sex.value}")
            
            if pc.race:
                print(f"Race: {pc.race.value}")
            
            if pc.age_min or pc.age_max:
                age = self.format_age(pc.age_min, pc.age_max)
                print(f"Age: {age}")
            
            # Location
            if record.location_found.state:
                location_parts = [record.location_found.city, record.location_found.county, record.location_found.state]
                location = ", ".join(filter(None, location_parts))
                print(f"Location: {location}")
            
            # Match reasons
            if result.match_reasons:
                print(f"Match reasons: {', '.join(result.match_reasons[:3])}")
            
            print(f"{Fore.BLUE}{'-'*40}{Style.RESET_ALL}")
        
        if len(results) > 10:
            print(f"\n{Fore.YELLOW}Showing top 10 of {len(results)} results.{Style.RESET_ALL}")
    
    def show_current_criteria(self):
        """Show current search criteria"""
        print(f"\n{Fore.GREEN}Current Search Criteria:{Style.RESET_ALL}")
        
        if not self.has_search_criteria():
            print(f"{Fore.YELLOW}No criteria set.{Style.RESET_ALL}")
            return
        
        # Physical characteristics
        pc = self.criteria.physical_characteristics
        print(f"\n{Fore.CYAN}Physical Characteristics:{Style.RESET_ALL}")
        
        if pc.height_min or pc.height_max:
            height = self.format_height(pc.height_min, pc.height_max)
            print(f"  Height: {height}")
        
        if pc.weight_min or pc.weight_max:
            weight = self.format_weight(pc.weight_min, pc.weight_max)
            print(f"  Weight: {weight}")
        
        if pc.sex:
            print(f"  Sex: {pc.sex.value}")
        
        if pc.race:
            print(f"  Race: {pc.race.value}")
        
        if pc.age_min or pc.age_max:
            age = self.format_age(pc.age_min, pc.age_max)
            print(f"  Age: {age}")
        
        if pc.distinguishing_marks:
            print(f"  Distinguishing marks: {', '.join(pc.distinguishing_marks)}")
        
        # Location
        loc = self.criteria.location
        if loc.state or loc.county or loc.city:
            print(f"\n{Fore.CYAN}Location Filters:{Style.RESET_ALL}")
            if loc.state:
                print(f"  State: {loc.state}")
            if loc.county:
                print(f"  County: {loc.county}")
            if loc.city:
                print(f"  City: {loc.city}")
    
    def clear_criteria(self):
        """Clear all search criteria"""
        self.criteria = SearchCriteria()
        print(f"{Fore.GREEN}All search criteria cleared.{Style.RESET_ALL}")
    
    def show_help(self):
        """Show help information"""
        print(f"\n{Fore.GREEN}Help & Instructions:{Style.RESET_ALL}")
        print(f"\n{Fore.CYAN}How to use this system:{Style.RESET_ALL}")
        print("1. Set physical characteristics of the person you're looking for")
        print("2. Optionally set location filters to narrow your search")
        print("3. Perform the search to find potential matches")
        print("4. Review results and follow up on promising matches")
        
        print(f"\n{Fore.CYAN}Tips for better results:{Style.RESET_ALL}")
        print("• Use ranges for height, weight, and age instead of exact values")
        print("• Start with broader criteria and narrow down if needed")
        print("• Include distinguishing marks if known (tattoos, scars, etc.)")
        print("• Try different location combinations")
        print("• Check multiple databases for comprehensive coverage")
        
        print(f"\n{Fore.CYAN}Available databases:{Style.RESET_ALL}")
        databases = self.search_engine.get_available_databases()
        for db in databases:
            print(f"• {db}")
    
    def show_ethics(self):
        """Show ethical guidelines"""
        print(f"\n{Fore.RED}ETHICAL USAGE GUIDELINES:{Style.RESET_ALL}")
        print(f"\n{Fore.YELLOW}This tool is designed to help reunite families with missing loved ones.")
        print("Please use it responsibly and ethically.{Style.RESET_ALL}")
        
        print(f"\n{Fore.CYAN}DO:{Style.RESET_ALL}")
        print("• Use this tool to help find missing family members")
        print("• Contact law enforcement with any potential matches")
        print("• Respect the privacy and dignity of the deceased")
        print("• Be patient and thorough in your search")
        
        print(f"\n{Fore.CYAN}DON'T:{Style.RESET_ALL}")
        print("• Use this for curiosity or entertainment")
        print("• Share sensitive information publicly")
        print("• Make assumptions based on limited information")
        print("• Contact families directly without law enforcement")
        
        print(f"\n{Fore.RED}Remember: This tool provides leads, not definitive identifications.")
        print("Always work with proper authorities for verification.{Style.RESET_ALL}")
    
    def show_goodbye(self):
        """Show goodbye message"""
        print(f"\n{Fore.BLUE}Thank you for using the Jane Doe Search System.")
        print("We hope this tool helps bring families together.{Style.RESET_ALL}")
    
    # Helper methods
    def get_height_input(self, prompt: str) -> Optional[int]:
        """Get height input in various formats"""
        value = input(prompt).strip()
        if not value:
            return None
        
        # Try feet'inches" format
        if "'" in value or '"' in value:
            import re
            match = re.search(r"(\d+)'?\s*(\d+)?", value)
            if match:
                feet = int(match.group(1))
                inches = int(match.group(2)) if match.group(2) else 0
                return feet * 12 + inches
        
        # Try plain inches
        try:
            return int(value)
        except ValueError:
            print(f"{Fore.RED}Invalid height format. Try '5'8\"' or '68'{Style.RESET_ALL}")
            return None
    
    def get_integer_input(self, prompt: str) -> Optional[int]:
        """Get integer input with validation"""
        value = input(prompt).strip()
        if not value:
            return None
        
        try:
            return int(value)
        except ValueError:
            print(f"{Fore.RED}Please enter a valid number.{Style.RESET_ALL}")
            return None
    
    def format_height(self, height_min: Optional[int], height_max: Optional[int]) -> str:
        """Format height for display"""
        if height_min and height_max and height_min != height_max:
            return f"{self.inches_to_feet_inches(height_min)} - {self.inches_to_feet_inches(height_max)}"
        elif height_min or height_max:
            height = height_min or height_max
            return self.inches_to_feet_inches(height)
        return "Unknown"
    
    def format_weight(self, weight_min: Optional[int], weight_max: Optional[int]) -> str:
        """Format weight for display"""
        if weight_min and weight_max and weight_min != weight_max:
            return f"{weight_min} - {weight_max} lbs"
        elif weight_min or weight_max:
            weight = weight_min or weight_max
            return f"{weight} lbs"
        return "Unknown"
    
    def format_age(self, age_min: Optional[int], age_max: Optional[int]) -> str:
        """Format age for display"""
        if age_min and age_max and age_min != age_max:
            return f"{age_min} - {age_max} years"
        elif age_min or age_max:
            age = age_min or age_max
            return f"{age} years"
        return "Unknown"
    
    def inches_to_feet_inches(self, total_inches: int) -> str:
        """Convert inches to feet'inches\" format"""
        feet = total_inches // 12
        inches = total_inches % 12
        return f"{feet}'{inches}\""
    
    def show_sex_options(self):
        """Show sex options"""
        print("1. Male")
        print("2. Female") 
        print("3. Unknown")
    
    def show_race_options(self):
        """Show race options"""
        print("1. White")
        print("2. Black/African American")
        print("3. Hispanic/Latino")
        print("4. Asian")
        print("5. Native American")
        print("6. Pacific Islander")
        print("7. Multiracial")
        print("8. Unknown")
    
    def has_search_criteria(self) -> bool:
        """Check if any search criteria are set"""
        pc = self.criteria.physical_characteristics
        loc = self.criteria.location
        
        return (pc.height_min or pc.height_max or pc.weight_min or pc.weight_max or
                pc.race or pc.sex or pc.age_min or pc.age_max or 
                pc.distinguishing_marks or loc.state or loc.county or loc.city)


def main():
    """Main entry point"""
    cli = CLIInterface()
    cli.run()


if __name__ == "__main__":
    main()