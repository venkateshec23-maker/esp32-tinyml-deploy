# Interview prep (P2)

## 2-minute explanation
"emlearn converts sklearn models to microcontroller C, but linear models were
missing. I implemented the missing converter — logistic and linear regression
to dependency-free C — with 8 parity tests proving the C matches sklearn
exactly on classes. I then built the full deployment pipeline around it: a
DHT comfort classifier for ESP32 with data collection, rule labeling, training
and a bake step. Without hardware I proved everything host-side: the classifier
firmware builds at plus-228 bytes of flash, and I documented exactly what's
pending. I also refused to fake results twice: latency numbers that were below
my timer's trust floor, and training labels that are rules, not discoveries."

## 10 questions
1. Why do linear models matter on MCUs when trees already exist? (code size,
   predict cost, interpretability)
2. How does your Wrapper map sklearn's coef_ to C for binary vs multinomial?
3. Why is argmax-over-logits exactly equal to argmax-over-softmax?
4. What does your (void)features_length fix say about -Werror in generated code?
5. Why didn't you use upstream CompiledClassifier in tests? (MSVC binding)
6. Your train accuracy is 0.8767, not 100% — why, and why is that fine?
7. What would break switching to fixed-point? (expf/softmax scaling, #77)
8. How do you know the baked firmware matches the trained model? (bake copies
   the tested artifact; hashes in a future step)
9. What fails first with single-class live data, and what does your pipeline do?
10. What part did YOU implement vs upstream, and where is the boundary file?
