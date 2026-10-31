import random

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

    if type(alphabet_size) is not int or alphabet_size < 2:
        raise ValueError("Alphabet size must be a positive integer bigger than 1")

    if any(type(collision) is not int for collision in additional_collisions):
        raise TypeError("List provide contains a non integer datatype.")

    if len(additional_collisions) + sum(additional_collisions)  > alphabet_size: 
        raise ValueError("Collision structure exceeds alphabet size.")

    if any(collision < 1 for collision in additional_collisions):
        raise ValueError("Each collision group must contain at least one additional symbol.")

    collision_source_amount = len(additional_collisions)

    source_ids = create_alphabet(alphabet_size)

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

def create_alphabet(base_n: int) -> list[int]:
    '''
    Changes the size of the symbol alphabet used in the experiment.

    Args:
        base_n: The desired alphabet size (base).

    Returns:
        An alphabet containing `base_n` distinct symbols.
    '''

    # Base 1 is theoretically possible, but a collision isn't. However no non-injective function exists to study.
    if type(base_n) is not int or base_n < 2:
        raise ValueError("B must be a positive integer.")

    return list(range(base_n))

def encode_string(
    text: str,
    alphabet: dict[str, int]
) -> list[int]:
    '''
    Encodes a string into a sequence of integer symbol IDs based on the provided alphabet.

    Args:
        text: The input string to encode.
        alphabet: A list of unique symbols defining the encoding alphabet.

    Returns:
        A list of integers representing the positions of the input symbols in the alphabet.
    '''

    resulting_text = []

    for char in text:
        symbol_id = alphabet.get(char)
        if symbol_id is None:
            raise ValueError(f"Character '{char}' is not in the alphabet.")
        resulting_text.append(symbol_id)

    return resulting_text

def apply_mapping(
    sequence: list[int],
    mapping: dict[int, int]
) -> list[int]:
    '''
    Applies a many-to-one substitution mapping to a sequence of integer symbol IDs.

    Args:
        sequence: The original sequence of source symbol IDs.
        mapping: A dictionary mapping each source symbol ID to an observed symbol ID.

    Returns:
        A new sequence containing the mapped symbol IDs, preserving the original order.
    '''

    encoded_sequence = []

    for char_id in sequence:
        encoded_id = mapping.get(char_id)
        if encoded_id is None:
            raise KeyError(f"No mapping defined for symbol ID {char_id}.")
        encoded_sequence.append((encoded_id))

    return encoded_sequence