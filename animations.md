# Notes
When sending a list of cards, there some require an ID and some do not.
If the card is already in your hand (eg an animation to remove or play from your hand), then the id is required.
Otherwise, just use an array of urls.
# Animations
### Play cards
This will draw the cards leaving your hand and going to the planning pile  
```
animate {  
  type: play cards  
  data: [{  
    id, card image url  
  }]  
}  
```

### Undo
This undos the top card in the planning pile  
```
animate {  
  type: undo  
}
```

### Undo all
Undos all cards in the planning pile
```
animate {  
  type: undo all  
}
```

### Pickup
Shows cards coming from either a player or the deck into your hand.
Note that only the deck has been implemented  
```
animate {  
  type: pickup  
  from: None (None = deck. Use player id for player (NOT IMPLEMENTED JUST USE None FOR NOW))  
  data: [url, url, url]  
}
```
### Remove cards
Shows cards leaving your hand and into the deck (TODO for future: allow the cards to be given to other players)  
```
animate {  
  type: remove cards  
  data: [{  
    id, card image url  
  }]  
}  
```

### Sound
Plays a sound  
```
animate {  
  type: sound  
  sound: /static/sounds/sound.mp3  
}
```

# Special Animations
These animations are only for specific cards  
### Communist
```
animate {  
  type: communist  
  your cards: [url, url, url]  // the cards you will be given afterwards  
}
```
### Thanos
```
animate {  
  type: thanos  
  data: [{  
    id, card image url  
  }]  
}
```
### Genocide
```
animate {  
  type: genocide  
  banned: Blue  // visual only, make this formatted with caps  
  cards to remove: [{  
    id, card image url  
  }]  
}
```
