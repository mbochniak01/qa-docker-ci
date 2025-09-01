import pytest
from app.spam_model import train_and_save_model, predict
import allure
from app.spam_model import predict_with_prob
@pytest.fixture(scope="module", autouse=True)
def setup_model():
    # Train & save model once before all tests
    train_and_save_model()

def test_predict_spam():
    text = "Congratulations! You've won a free lottery"
    label, probs = predict_with_prob(text)
    
    # Attach prediction details to Allure
    allure.attach(
        body=f"Text: {text}\nPredicted label: {label}\nProbabilities: {probs}",
        name="Spam prediction details",
        attachment_type=allure.attachment_type.TEXT
    )
    assert label.lower() == "spam"

def test_predict_ham():
    text = "Hey, are we still meeting tomorrow?"
    label = predict(text)
    assert label.lower() == "ham"

def test_predict_edge_case():
    text = ""
    label = predict(text)
    # should not crash, may default to ham or spam
    assert label.lower() in ["ham", "spam"]

# ---------- Borderline spam cases ----------

def test_predict_borderline_1():
    text = "Reminder: Your appointment is tomorrow, confirm your spot."
    label = predict(text)
    # Could be ham, but looks a bit like automated message
    assert label.lower() in ["ham", "spam"]

def test_predict_borderline_2():
    text = "Limited offer: Buy one get one free at your local store!"
    label = predict(text)
    assert label.lower() in ["spam", "ham"]

def test_predict_borderline_3():
    text = "Hey, did you check out the new discounts online?"
    label = predict(text)
    assert label.lower() in ["ham", "spam"]
