import random
from collections import Counter

def make_mapping(
    alphabet_size: int, 
    additional_collisions: list,
    random_generator: random.Random
) -> dict[int, int]:
    '''
    Creates a dictonary representing a many-to-one substitution.

    args: 
        alphabet_size: Number of symbols in the source alphabet.
        additional_collisions: List of natural numbers how many more letters should collide into the same ciphered letter.
        random_generator: Random number generator used for reproducibility.

    returns:
        A dictionary mapping each source symbol ID to an observed symbol ID.
    '''

    if type(alphabet_size) is not int or alphabet_size < 1:
        raise ValueError("Alphabet size must be a positive integer.")

    if any(type(collision) is not int for collision in additional_collisions):
        raise TypeError("List provide contains a non integer datatype.")

    if len(additional_collisions) + sum(additional_collisions)  > alphabet_size: 
        raise ValueError("Collision structure exceeds alphabet size.")

    if any(collision < 1 for collision in additional_collisions):
        raise ValueError("Each collision group must contain at least one additional symbol.")

    collision_source_amount = len(additional_collisions)

    source_ids = list(range(alphabet_size))

    # Letters that will be collided with.
    collision_roots = random_generator.sample(
        population = source_ids, 
        k = collision_source_amount
    )

    available_source_ids = [
        source_id for source_id in source_ids
        if source_id not in collision_roots
    ]

    # ID after substitution of root and its collision
    observed_results = random_generator.sample(
        population = source_ids, 
        k = collision_source_amount
    )
    
    mapping = {}

    for i in range(len(additional_collisions)):
        root = collision_roots[i]
        ciphered_root = observed_results[i]

        mapping[root] = ciphered_root

        collides_with = random_generator.sample(
            population = available_source_ids, 
            k = additional_collisions[i]
        )

        for collision in collides_with:
            mapping[collision] = ciphered_root 

        available_source_ids = [
            source_id for source_id in available_source_ids
            if source_id not in collides_with
        ]

    available_observed_results = [
        source_id for source_id in source_ids
        if source_id not in observed_results
    ]

    random_generator.shuffle(available_observed_results)

    for source, observed in zip(available_source_ids, available_observed_results):
        mapping[source] = observed

    return mapping