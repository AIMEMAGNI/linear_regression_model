import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

void main() {
  runApp(TVPricePredictorApp());
}

class TVPricePredictorApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'TV Price Predictor',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: PricePredictionScreen(),
    );
  }
}

class PricePredictionScreen extends StatefulWidget {
  @override
  _PricePredictionScreenState createState() => _PricePredictionScreenState();
}

class _PricePredictionScreenState extends State<PricePredictionScreen> {
  final TextEditingController brandController = TextEditingController();
  final TextEditingController resolutionController = TextEditingController();
  final TextEditingController sizeController = TextEditingController();
  final TextEditingController operatingSystemController =
      TextEditingController();

  String predictionResult = '';
  bool isLoading = false;

  Future<void> predictPrice() async {
    final String apiUrl =
        'https://tv-prices-api.onrender.com/predict'; // Change this to your actual API endpoint

    if (brandController.text.isEmpty ||
        resolutionController.text.isEmpty ||
        sizeController.text.isEmpty ||
        operatingSystemController.text.isEmpty) {
      setState(() {
        predictionResult = 'Please fill in all fields.';
      });
      return;
    }

    setState(() {
      isLoading = true;
    });

    // Dismiss the keyboard
    FocusScope.of(context).unfocus();

    try {
      final response = await http.post(
        Uri.parse(apiUrl),
        headers: {'Content-Type': 'application/json'},
        body: json.encode({
          'Brand': brandController.text,
          'Resolution': resolutionController.text,
          'Size': int.parse(sizeController.text),
          'Operating_System': operatingSystemController.text,
        }),
      );

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        setState(() {
          double predictedPrice = data['predicted_price'];
          predictionResult =
              'Predicted Price: \$${predictedPrice.abs().toStringAsFixed(2)}';
        });
      } else {
        setState(() {
          predictionResult = 'Error: ${response.reasonPhrase}';
        });
      }
    } catch (e) {
      setState(() {
        predictionResult = 'An error occurred: $e';
      });
    } finally {
      setState(() {
        isLoading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('TV Price Predictor'),
      ),
      body: SingleChildScrollView(
        child: Padding(
          padding: const EdgeInsets.all(16.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              TextField(
                controller: brandController,
                decoration: InputDecoration(labelText: 'Brand'),
              ),
              TextField(
                controller: resolutionController,
                decoration: InputDecoration(labelText: 'Resolution'),
              ),
              TextField(
                controller: sizeController,
                decoration: InputDecoration(labelText: 'Size'),
                keyboardType: TextInputType.number,
              ),
              TextField(
                controller: operatingSystemController,
                decoration: InputDecoration(labelText: 'Operating System'),
              ),
              SizedBox(height: 20),
              ElevatedButton(
                onPressed: isLoading ? null : predictPrice,
                child:
                    isLoading ? CircularProgressIndicator() : Text('Predict'),
              ),
              SizedBox(height: 20),
              Text(
                predictionResult,
                style: TextStyle(fontSize: 18),
                textAlign: TextAlign.center,
              ),
            ],
          ),
        ),
      ),
    );
  }
}
