import random

def detectItems():
    """
    We will simulate detecting items in a fridge.
    We will return a list of detected food items.
    How advanced the simulation is, depends on how far we take this project.
    
    """
    
    # A list/database of possible food items. will configure to have logic that ensures recipes make sense
    allPossibleItems = [
        "apple", "milk", "bread", "cheese", "eggs", "butter", "carrots",
        "tomatoes", "potatoes", "yogurt", "chicken", "fish", "rice", "pasta"
    ]
    
    # Randomly select 3-7 items from list.
    detectedItems = random.sample(allPossibleItems, random.randint(3, 7))
    return detectedItems

def runSimulation():
    
    items = detectItems()
    print("Detected items", items)
    
    
if __name__ == "__main__":
    runSimulation()
    
    