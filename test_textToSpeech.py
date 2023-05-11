import pytest
from textToVoice import get_list

def test_get_list():
    assert get_list("https://agigames.cz/apiout/test_prijmeni.php") == ["rambo", "Řepka", "mezerní", "tabulatorník", "mezeranakonci"]