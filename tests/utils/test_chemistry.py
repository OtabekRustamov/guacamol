from guacamol.utils.chemistry import canonicalize, canonicalize_list, is_valid


def test_validity_empty_molecule():
    smiles = ''
    assert not is_valid(smiles)


def test_validity_incorrect_syntax():
    smiles = 'CCCincorrectsyntaxCCC'
    assert not is_valid(smiles)


def test_validity_incorrect_valence():
    smiles = 'CCC(CC)(CC)(=O)CCC'
    assert not is_valid(smiles)


def test_validity_correct_molecules():
    smiles_1 = 'O'
    smiles_2 = 'C'
    smiles_3 = 'CC(ONONOC)CCCc1ccccc1'

    assert is_valid(smiles_1)
    assert is_valid(smiles_2)
    assert is_valid(smiles_3)


def test_isomeric_canonicalisation():
    endiandric_acid = 'OC(=O)[C@H]5C2\C=C/C3[C@@H]5CC4[C@H](C\C=C\C=C\c1ccccc1)[C@@H]2[C@@H]34'

    with_stereocenters = canonicalize(endiandric_acid, include_stereocenters=True)
    without_stereocenters = canonicalize(endiandric_acid, include_stereocenters=False)

    expected_with_stereocenters = 'O=C(O)[C@H]1C2C=CC3[C@@H]1CC1[C@H](C/C=C/C=C/c4ccccc4)[C@@H]2[C@@H]31'
    expected_without_stereocenters = 'O=C(O)C1C2C=CC3C1CC1C(CC=CC=Cc4ccccc4)C2C31'

    assert with_stereocenters == expected_with_stereocenters
    assert without_stereocenters == expected_without_stereocenters


def test_list_canonicalization_removes_none():
    m1 = 'CCC(OCOCO)CC(=O)NCC'
    m2 = 'this.is.not.a.molecule'
    m3 = 'c1ccccc1'
    m4 = 'CC(OCON=N)CC'

    molecules = [m1, m2, m3, m4]
    canonicalized_molecules = canonicalize_list(molecules)

    valid_molecules = [m1, m3, m4]
    expected = [canonicalize(smiles) for smiles in valid_molecules]

    assert canonicalized_molecules == expected