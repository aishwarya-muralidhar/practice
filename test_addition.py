
import pytest 
from addition import div

def test_div_positive_number():
    assert div(10,2) == 5

def test_div_negative_number():
    assert div(-6, 3) == -2

def test_div_floating_number():
    assert div(10, 4) == 2.5

def test_div_divide_by_zero_raises_error():
    with pytest.raises(ValueError) as excepinfo:
        div(10,0)
    assert "Cannot divide by zero" in str(excepinfo.value)
   
def test_div_zero_by_div():
    assert div(0,10) == 0