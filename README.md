  Current TODO:
    add colour set functionality? add to spreadsheet, find data, double check existing
    add tax, go functionality to Action: i.e. tax = -100, -200, go = 200
    auction
    houses
    bankruptcy test
    not enough money options
    build houses + hotels wrt colour sets
    sell houses + hotels wrt colour sets
    mortgaging
    action: chance, community chest
Automated banking system? No need for Bank class
No need for title deed cards, build directly into Property
Property packs: change between Monopoly versions - may affect chance and community chest Cards

CONSTRUCTS:
Players: 2 - 8, each with a Token, starts with $1500
(ignore: money limit)
Dice: 2, roll doubles (3 = go to jail)
Buildings: (Hotels: 12 & Houses: 32)
Chance and Community Chest cards
Title Deed Cards per Property

Everyone starts at go, highest roller starts
Land on square: buy unowned property, get banker to auction it, pay rent, pay taxes, (roll 3 dice) for community chest and chance, go to jail
collect $200 when you pass go
keep playing until one player left
(roll double (move then no extra turns) / wait 3 turns / pay fine = $50 / get out of jail free card)   4 get out jail free cards

can mortgage and sell property (even when mortgaged) to pay off debts or go bankrupt
can't borrow or lend money to another player, can accept property as payment

3 property types: station, streets, utilities
Buy property at face value
Auctions start at 10, original player can join bidding, increase by at least 1
1 utility = 4x dice roll, both = 10x dice roll
station rent based on number of stations that player owns

can buy house in between anyone's turn
Only build if own all of colour group
Each property of group increases builds at one time, max 4 Houses (evenly break down as well)
1 hotel from 4 houses (1 hotel == max)
charge extra on colour set (even if 1/2 mortgaged)
Can't build if 1 property of set is mortgaged
(ignore: limit of houses + hotels)

can't sell street if building on it, sell building to bank at 1/2 original purchase price
Can sell in between anyone's turn
Sell hotel: 1/2 hotel price + 1/2 price of 4 houses you swapped for it
Can break down hotel to 4 houses: 1/2 price

can't collect rent on mortgaged property, but can on rest of set
unmortgage: pay 110% of mortgage (double-check)

bankruptcy:
if owe the bank: return title deeds, auctioned off to players, mortgages cancelled
if owe another player: sell buildings to bank (1/2 price), give player GOJF cards, title deeds, remaining money

Chance and community chest, normal
Free parking
Passing go twice in one turn, collect 2x$200

Can collect rent in jail
get out of jail: pay 50, GOJF card (only on turn 1 and 2), roll double (move that number), 3 attempts else pay 50 move that number of spaces (3rd attempt) immediately
just visiting factor
