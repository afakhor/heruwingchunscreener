import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:candlesticks/candlesticks.dart'; // Pastikan sudah di pubspec.yaml

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
const MyApp({super.key});
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'Stock Screener Pro',
      theme: ThemeData(primarySwatch: Colors.blue),
      home: HomePage(),
    );
  }
}

class HomePage extends StatefulWidget {
  @override
  _HomePageState createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  List stocks = [];
  bool isLoading = true;

  @override
  void initState() {
    super.initState();
    fetchData();
  }

  Future<void> fetchData() async {
    try {
      final response = await http.get(Uri.parse('http://127.0.0.1:5000/api/stocks'));
      if (response.statusCode == 200) {
        setState(() {
          stocks = json.decode(response.body)['stocks'];
          isLoading = false;
        });
      }
    } catch (e) {
      print("Error koneksi: $e");
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text("Stock Screener Engine")),
      body: isLoading 
          ? Center(child: CircularProgressIndicator())
          : ListView.builder(
              itemCount: stocks.length,
              itemBuilder: (context, index) {
                final stock = stocks[index];
                double rsiValue = (stock['rsi'] ?? 0).toDouble();

                return Card(
                  margin: EdgeInsets.all(8),
                  child: ListTile(
                    title: Text(stock['ticker'], style: TextStyle(fontWeight: FontWeight.bold)),
                    subtitle: Text("Price: Rp ${stock['close']}"),
                    trailing: Container(
                      padding: EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                      decoration: BoxDecoration(
                        color: rsiValue > 70 ? Colors.red[100] : (rsiValue < 30 ? Colors.green[100] : Colors.grey[200]),
                        borderRadius: BorderRadius.circular(10),
                      ),
                      child: Text(
                        "RSI: ${rsiValue.toStringAsFixed(1)}",
                        style: TextStyle(
                          fontWeight: FontWeight.bold,
                          color: rsiValue > 70 ? Colors.red : (rsiValue < 30 ? Colors.green : Colors.black),
                        ),
                      ),
                    ),
                    onTap: () {
                      Navigator.push(
                        context,
                        MaterialPageRoute(
                          builder: (context) => StockChartPage(ticker: stock['ticker']),
                        ),
                      );
                    },
                  ),
                );
              },
            ),
      floatingActionButton: FloatingActionButton(
        onPressed: fetchData,
        child: Icon(Icons.refresh),
      ),
    );
  }
}

// Halaman Chart
class StockChartPage extends StatefulWidget {
  final String ticker;
  StockChartPage({required this.ticker});

  @override
  _StockChartPageState createState() => _StockChartPageState();
}

class _StockChartPageState extends State<StockChartPage> {
  List<Candle> candles = [];

  @override
  void initState() {
    super.initState();
    fetchChart();
  }

  Future<void> fetchChart() async {
    final response = await http.get(Uri.parse('http://127.0.0.1:5000/api/chart/${widget.ticker}'));
    if (response.statusCode == 200) {
      List data = json.decode(response.body);
      setState(() {
        candles = data.map((e) => Candle(
          date: DateTime.parse(e['date']),
          high: e['high'].toDouble(),
          low: e['low'].toDouble(),
          open: e['open'].toDouble(),
          close: e['close'].toDouble(),
          volume: e['volume'].toDouble(),
        )).toList().reversed.toList();
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text(widget.ticker)),
      body: candles.isEmpty 
          ? Center(child: CircularProgressIndicator()) 
          : Candlesticks(candles: candles),
    );
  }
}