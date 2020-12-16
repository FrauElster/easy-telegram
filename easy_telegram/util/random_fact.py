from random import randint


def random_fact() -> str:
    facts = [
        "Some cats are allergic to humans",
        "Competitive art was an olypiadic discipline",
        "A chef's hat has exactly 100 folds",
        "Oranges are not naturally occurring fruits",
        "High Heels were originally worn by men",
        "Queen Elizabth II is a trained mechanic",
        "2014 was the first Tinder Match on the Antarctic",
        "Hot water freezes faster than cold water",
        "Dolphins have names for each other",
        "Otters holding hands while sleeping",
        "The national animal of Scotland is a unicorn",
        "Bees sometimes sting other bees",
        "Koalas have fingerprints",
        "The author of Dracula was never in Transylvania",
        "Humans sneeze faster than cheetahs",
        "The patent for hydrants was lost in a fire",
        "Cows kill more people than sharks",
        "Sharks have been around longer than trees",
        "The Twitter bird's name is Larry",
        "Banging your head against the wall burns about 150 calories",
        "When hippos are angry, their sweat is red",
        "A flock of crows is called \"murderer\"",
        "The average woman uses about 34cm of lipstick per year",
        "If you lift a kangaroo's tail, it cannot hop",
        "Catfish are the only animals with an uneven number of whiskers",
        "The French language has 7 different words for \"surrender\"",
        "The Eifel Tower has 1665 steps",
        "Los Angeles is actually called \n\"El Pueblo de Nuestra Senora la Reina de los Angeles\""
    ]

    return facts[randint(0, len(facts) - 1)]
