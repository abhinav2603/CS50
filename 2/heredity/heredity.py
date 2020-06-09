import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    #raise NotImplementedError
    d = {
        person: {
            "gene": 0,
            "trait": False
        }
        for person in people
    }
    for person in one_gene:
        d[person]["gene"]=1
    for person in two_genes:
        d[person]["gene"]=2
    for person in have_trait:
        d[person]["trait"]=True

    d1 = {}
    for person in people:
        if people[person]["mother"] is None:
            prob_gene = PROBS["gene"][d[person]["gene"]]
            prob_trait = PROBS["trait"][d[person]["gene"]][d[person]["trait"]]
            d1[person] = prob_gene * prob_trait
        else:
            prob_trait = PROBS["trait"][d[person]["gene"]][d[person]["trait"]]
            mother = people[person]["mother"]
            father = people[person]["father"]
            m_gene = d[mother]["gene"]
            f_gene = d[father]["gene"]
            g11 = [m_gene,f_gene]
            s_gene = d[person]["gene"]
            prob_gene = 0
            l = []
            if s_gene == 0:
                l = [[0,0]]
            elif s_gene == 1:
                l = [[0,1],[1,0]]
            else:
                l = [[1,1]]
            for g22 in l:
                # g22 = [m1,s_gene-m1]
                p = [1,1]
                for i in range(2):
                    if  g11[i] == 2:
                        if g22[i] == 1:
                            p[i] = 1-PROBS["mutation"]
                        else:
                            p[i] = PROBS["mutation"]
                    elif g11[i] == 1:
                        if g22[i] == 1:
                            p[i] = .5
                        else:
                            p[i] = .5
                    else:
                        if g22[i] == 0:
                            p[i] = 1-PROBS["mutation"]
                        else:
                            p[i] = PROBS["mutation"]
                prob_gene += p[0]*p[1]

            d1[person] = prob_gene * prob_trait
    pr=1
    for k in d1:
        pr *= d1[k]
    return pr

def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    #raise NotImplementedError
    d = {
        person: {
            "gene": 0,
            "trait": False
        }
        for person in probabilities
    }
    for people in one_gene:
        d[people]["gene"]=1
    for people in two_genes:
        d[people]["gene"]=2
    for people in have_trait:
        d[people]["trait"]=True

    for people in probabilities:
        probabilities[people]["gene"][d[people]["gene"]] += p
        probabilities[people]["trait"][d[people]["trait"]] += p


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    #raise NotImplementedError
    for people in probabilities:
        sum1 = 0
        for g in probabilities[people]["gene"]:
            sum1 += probabilities[people]["gene"][g]
        for g in probabilities[people]["gene"]:
            probabilities[people]["gene"][g] /= sum1
        sum1 = 0
        for t in probabilities[people]["trait"]:
            sum1 += probabilities[people]["trait"][t]
        for t in probabilities[people]["trait"]:
            probabilities[people]["trait"][t] /= sum1


if __name__ == "__main__":
    main()
