# Card transfer
Default card transfer animations can be easily called using game.animate_card_transfer()  
  
NOTE:  
Removing a card from your hand must include the card id  
Adding a card to your hand must include the card name and id

### Play cards
This will draw the cards leaving your hand and going to the planning pile  
```
animate {  
  type: play cards  
  cards: [{  
    id, card image url  
  }]  
}  
```

### Pickup
Shows cards coming from either a player or the deck into your hand.
Note that only the deck has been implemented  
```
animate {  
  type: pickup  
  from: None (None = deck. Use player id for player (NOT IMPLEMENTED JUST USE None FOR NOW))  
  cards: [{  
    id, name, card image url  
  }]  
}
```
### Remove cards
Shows cards leaving your hand and into the deck (TODO for future: allow the cards to be given to other players)  
```
animate {  
  type: remove cards  
  cards: [{  
    id, card image url  
  }]  
}  
```
# Miscellaneous Animations

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
  cards: [{  
    id, name, card image url  
  }]    // the cards you will be given afterwards  
}
```
### Thanos
```
animate {  
  type: thanos  
  cards: [{  
    id, card image url  
  }]  
}
```
### Genocide
```
animate {  
  type: genocide  
  banned: Blue  // visual only, make this formatted with caps  
  cards: [{  
    id, card image url  
  }]  
}
```
