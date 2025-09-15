# Flutter App Structure - Weighing System

## 📱 Project Architecture Overview

```
weighing_app/
├── lib/
│   ├── main.dart
│   ├── app.dart
│   ├── core/
│   ├── features/
│   ├── shared/
│   └── config/
├── assets/
├── test/
└── pubspec.yaml
```

---

## 🏗️ Core Architecture Pattern

**Clean Architecture + Riverpod + Repository Pattern**

- **Presentation Layer**: UI + Riverpod Providers (State Management)
- **Domain Layer**: Business Logic + Use Cases
- **Data Layer**: Repository + Data Sources (Supabase, Local Storage)

---

## 📁 Detailed Folder Structure

### `/lib/core/` - Core Utilities & Constants

```
lib/core/
├── constants/
│   ├── app_constants.dart          # App-wide constants
│   ├── api_constants.dart          # API endpoints
│   ├── storage_constants.dart      # Local storage keys
│   └── ui_constants.dart           # UI constants (colors, sizes)
├── errors/
│   ├── exceptions.dart             # Custom exceptions
│   ├── failures.dart               # Failure classes
│   └── error_handler.dart          # Global error handling
├── network/
│   ├── network_info.dart           # Network connectivity check
│   ├── supabase_client.dart        # Supabase client setup
│   └── api_interceptor.dart        # Request/Response interceptor
├── utils/
│   ├── date_utils.dart             # Date formatting utilities
│   ├── weight_calculator.dart      # Weight calculation logic
│   ├── qr_generator.dart           # QR code generation
│   ├── validators.dart             # Form validators
│   └── extensions.dart             # Dart extensions
└── services/
    ├── scale_service.dart          # Scale hardware integration
    ├── printer_service.dart        # Label printer service
    ├── permission_service.dart     # Device permissions
    └── notification_service.dart   # Local notifications
```

### `/lib/config/` - App Configuration

```
lib/config/
├── app_config.dart                 # Environment configuration
├── router.dart                     # App routing (GoRouter)
├── theme.dart                      # App themes & styling
├── injection.dart                  # Dependency injection (GetIt)
└── supabase_config.dart           # Supabase configuration
```

### `/lib/shared/` - Shared Components

```
lib/shared/
├── widgets/
│   ├── custom_app_bar.dart         # Reusable app bar
│   ├── loading_widget.dart         # Loading indicators
│   ├── error_widget.dart           # Error display widget
│   ├── custom_button.dart          # Styled buttons
│   ├── custom_text_field.dart      # Styled text inputs
│   ├── weight_display.dart         # Weight value display
│   ├── qr_scanner_widget.dart      # QR code scanner
│   └── confirmation_dialog.dart    # Confirmation dialogs
├── models/
│   ├── api_response.dart           # Generic API response
│   ├── user_session.dart           # User session data
│   └── app_state.dart              # Global app state
└── mixins/
    ├── validation_mixin.dart       # Form validation mixin
    ├── permission_mixin.dart       # Permission handling mixin
    └── scale_connection_mixin.dart # Scale connection helpers
```

---

## 🎯 Feature-Based Structure

### `/lib/features/auth/` - Authentication

```
features/auth/
├── data/
│   ├── datasources/
│   │   ├── auth_remote_datasource.dart
│   │   └── auth_local_datasource.dart
│   ├── models/
│   │   ├── user_model.dart
│   │   └── login_response_model.dart
│   └── repositories/
│       └── auth_repository_impl.dart
├── domain/
│   ├── entities/
│   │   └── user.dart
│   ├── repositories/
│   │   └── auth_repository.dart
│   └── usecases/
│       ├── login_usecase.dart
│       ├── logout_usecase.dart
│       └── get_current_user_usecase.dart
└── presentation/
    ├── providers/
    │   ├── auth_provider.dart
    │   ├── auth_state_provider.dart
    │   └── user_provider.dart
    ├── pages/
    │   ├── login_page.dart
    │   ├── splash_page.dart
    │   └── profile_page.dart
    └── widgets/
        ├── login_form.dart
        └── user_avatar.dart
```

### `/lib/features/sku/` - SKU Management

```
features/sku/
├── data/
│   ├── datasources/
│   │   ├── sku_remote_datasource.dart
│   │   └── sku_local_datasource.dart
│   ├── models/
│   │   └── sku_model.dart
│   └── repositories/
│       └── sku_repository_impl.dart
├── domain/
│   ├── entities/
│   │   └── sku.dart
│   ├── repositories/
│   │   └── sku_repository.dart
│   └── usecases/
│       ├── get_sku_list_usecase.dart
│       ├── search_sku_usecase.dart
│       ├── get_sku_details_usecase.dart
│       └── create_sku_usecase.dart
└── presentation/
    ├── providers/
    │   ├── sku_list_provider.dart
    │   ├── sku_search_provider.dart
    │   ├── selected_sku_provider.dart
    │   └── sku_form_provider.dart
    ├── pages/
    │   ├── sku_list_page.dart
    │   ├── sku_detail_page.dart
    │   ├── sku_search_page.dart
    │   └── sku_form_page.dart
    └── widgets/
        ├── sku_card.dart
        ├── sku_search_bar.dart
        └── sku_info_display.dart
```

### `/lib/features/weighing/` - Main Weighing Feature

```
features/weighing/
├── data/
│   ├── datasources/
│   │   ├── weighing_remote_datasource.dart
│   │   ├── weighing_local_datasource.dart
│   │   └── scale_datasource.dart
│   ├── models/
│   │   ├── weighing_transaction_model.dart
│   │   ├── container_model.dart
│   │   └── scale_reading_model.dart
│   └── repositories/
│       ├── weighing_repository_impl.dart
│       └── scale_repository_impl.dart
├── domain/
│   ├── entities/
│   │   ├── weighing_transaction.dart
│   │   ├── container.dart
│   │   └── scale_reading.dart
│   ├── repositories/
│   │   ├── weighing_repository.dart
│   │   └── scale_repository.dart
│   └── usecases/
│       ├── create_weighing_transaction_usecase.dart
│       ├── get_scale_reading_usecase.dart
│       ├── calculate_net_weight_usecase.dart
│       ├── validate_qc_usecase.dart
│       └── save_transaction_usecase.dart
└── presentation/
    ├── providers/
    │   ├── weighing_provider.dart
    │   ├── scale_provider.dart
    │   ├── qc_provider.dart
    │   ├── container_provider.dart
    │   └── weighing_form_provider.dart
    ├── pages/
    │   ├── weighing_main_page.dart
    │   ├── container_selection_page.dart
    │   └── weighing_result_page.dart
    └── widgets/
        ├── weight_display_widget.dart
        ├── scale_connection_widget.dart
        ├── qc_status_widget.dart
        ├── calculation_display.dart
        └── transaction_form.dart
```

### `/lib/features/reports/` - Reports & Analytics

```
features/reports/
├── data/
│   ├── datasources/
│   │   └── report_remote_datasource.dart
│   ├── models/
│   │   ├── report_data_model.dart
│   │   └── chart_data_model.dart
│   └── repositories/
│       └── report_repository_impl.dart
├── domain/
│   ├── entities/
│   │   ├── report_data.dart
│   │   └── chart_data.dart
│   ├── repositories/
│   │   └── report_repository.dart
│   └── usecases/
│       ├── get_transaction_report_usecase.dart
│       ├── get_chart_data_usecase.dart
│       └── export_report_usecase.dart
└── presentation/
    ├── providers/
    │   ├── report_provider.dart
    │   ├── chart_data_provider.dart
    │   ├── report_filter_provider.dart
    │   └── export_provider.dart
    ├── pages/
    │   ├── dashboard_page.dart
    │   ├── report_list_page.dart
    │   └── chart_detail_page.dart
    └── widgets/
        ├── dashboard_card.dart
        ├── chart_widget.dart
        ├── report_filter.dart
        └── export_button.dart
```

### `/lib/features/printing/` - Label Printing

```
features/printing/
├── data/
│   ├── datasources/
│   │   ├── printer_datasource.dart
│   │   └── template_datasource.dart
│   ├── models/
│   │   ├── label_template_model.dart
│   │   └── print_job_model.dart
│   └── repositories/
│       └── printing_repository_impl.dart
├── domain/
│   ├── entities/
│   │   ├── label_template.dart
│   │   └── print_job.dart
│   ├── repositories/
│   │   └── printing_repository.dart
│   └── usecases/
│       ├── generate_label_usecase.dart
│       ├── print_label_usecase.dart
│       └── get_printer_status_usecase.dart
└── presentation/
    ├── providers/
    │   ├── printing_provider.dart
    │   ├── printer_connection_provider.dart
    │   ├── label_template_provider.dart
    │   └── print_queue_provider.dart
    ├── pages/
    │   ├── label_preview_page.dart
    │   └── printer_settings_page.dart
    └── widgets/
        ├── label_preview_widget.dart
        ├── printer_connection_widget.dart
        └── print_queue_widget.dart
```

---

## 📦 Key Dependencies (pubspec.yaml)

```yaml
dependencies:
  flutter:
    sdk: flutter
  
  # State Management
  flutter_riverpod: ^2.4.5
  riverpod_annotation: ^2.3.0
  
  # Network & Database
  supabase_flutter: ^2.0.0
  dio: ^5.3.2
  connectivity_plus: ^5.0.1
  
  # Storage
  shared_preferences: ^2.2.2
  hive: ^2.2.3
  hive_flutter: ^1.1.0
  
  # UI Components
  flutter_screenutil: ^5.9.0
  cached_network_image: ^3.3.0
  shimmer: ^3.0.0
  
  # Navigation
  go_router: ^12.1.1
  
  # Dependency Injection
  get_it: ^7.6.4
  injectable: ^2.3.2
  
  # Hardware Integration
  flutter_bluetooth_serial: ^0.4.0
  qr_code_scanner: ^1.0.1
  qr_flutter: ^4.1.0
  
  # Charts & Graphics
  fl_chart: ^0.65.0
  syncfusion_flutter_charts: ^23.1.36
  
  # Printing
  esc_pos_utils: ^1.1.0
  esc_pos_bluetooth: ^0.4.1
  
  # File Handling
  path_provider: ^2.1.1
  csv: ^5.0.2
  pdf: ^3.10.7
  
  # Utils
  intl: ^0.18.1
  uuid: ^4.1.0
  permission_handler: ^11.0.1

dev_dependencies:
  flutter_test:
    sdk: flutter
  build_runner: ^2.4.7
  riverpod_generator: ^2.3.0
  riverpod_lint: ^2.3.0
  custom_lint: ^0.5.0
  injectable_generator: ^2.4.1
  hive_generator: ^2.0.1
  mockito: ^5.4.2
```

---

## 🎨 UI Theme Structure

### `/lib/config/theme.dart`

```dart
class AppTheme {
  static ThemeData lightTheme = ThemeData(
    primarySwatch: Colors.blue,
    scaffoldBackgroundColor: AppColors.background,
    appBarTheme: AppBarTheme(
      backgroundColor: AppColors.primary,
      elevation: 0,
      titleTextStyle: AppTextStyles.heading,
    ),
    elevatedButtonTheme: ElevatedButtonThemeData(
      style: ElevatedButton.styleFrom(
        backgroundColor: AppColors.primary,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(8),
        ),
      ),
    ),
  );
  
  static ThemeData darkTheme = ThemeData.dark().copyWith(
    // Dark theme configuration
  );
}

class AppColors {
  static const Color primary = Color(0xFF1976D2);
  static const Color secondary = Color(0xFF42A5F5);
  static const Color error = Color(0xFFE53935);
  static const Color warning = Color(0xFFFF9800);
  static const Color success = Color(0xFF4CAF50);
  static const Color background = Color(0xFFF5F5F5);
  static const Color surface = Color(0xFFFFFFFF);
}

class AppTextStyles {
  static const TextStyle heading = TextStyle(
    fontSize: 20,
    fontWeight: FontWeight.bold,
  );
  
  static const TextStyle body = TextStyle(
    fontSize: 16,
    fontWeight: FontWeight.normal,
  );
  
  static const TextStyle caption = TextStyle(
    fontSize: 14,
    fontWeight: FontWeight.w400,
    color: Colors.grey,
  );
}
```

---

## 🔄 State Management Pattern (Riverpod)

### Provider Types & Usage:

```dart
// 1. Provider - For immutable data
@riverpod
String apiBaseUrl(ApiBaseUrlRef ref) {
  return 'https://your-supabase-url.supabase.co';
}

// 2. FutureProvider - For async data
@riverpod
Future<List<Sku>> skuList(SkuListRef ref) async {
  final repository = ref.read(skuRepositoryProvider);
  return await repository.getAllSkus();
}

// 3. StreamProvider - For real-time data
@riverpod
Stream<List<WeighingTransaction>> realtimeTransactions(RealtimeTransactionsRef ref) {
  final supabase = ref.read(supabaseClientProvider);
  return supabase
      .from('weighing_transaction')
      .stream(primaryKey: ['id'])
      .map((data) => data.map((json) => WeighingTransaction.fromJson(json)).toList());
}

// 4. StateNotifierProvider - For complex state
@riverpod
class WeighingNotifier extends _$WeighingNotifier {
  @override
  WeighingState build() {
    return const WeighingState.initial();
  }

  Future<void> loadSku(String skuId) async {
    state = const WeighingState.loading();
    try {
      final repository = ref.read(skuRepositoryProvider);
      final sku = await repository.getSkuById(skuId);
      state = WeighingState.loaded(selectedSku: sku);
    } catch (e) {
      state = WeighingState.error(e.toString());
    }
  }

  Future<void> readScaleWeight() async {
    final scaleService = ref.read(scaleServiceProvider);
    final weight = await scaleService.getCurrentWeight();
    
    state = state.copyWith(
      currentWeight: weight,
      netWeight: weight - (state.selectedContainer?.weight ?? 0),
    );
  }

  void selectContainer(Container container) {
    state = state.copyWith(selectedContainer: container);
  }
}

// 5. StateProvider - For simple state
final selectedSkuIdProvider = StateProvider<String?>((ref) => null);
final scaleConnectionStatusProvider = StateProvider<bool>((ref) => false);
```

### State Classes with Freezed:

```dart
@freezed
class WeighingState with _$WeighingState {
  const factory WeighingState.initial() = WeighingInitial;
  const factory WeighingState.loading() = WeighingLoading;
  const factory WeighingState.loaded({
    Sku? selectedSku,
    Container? selectedContainer,
    double? currentWeight,
    double? netWeight,
    int? calculatedPieces,
    QcStatus? qcStatus,
  }) = WeighingLoaded;
  const factory WeighingState.error(String message) = WeighingError;
}
```

---

## 🔌 Dependency Injection Setup (Riverpod + GetIt)

### `/lib/config/providers.dart`

```dart
import 'package:riverpod_annotation/riverpod_annotation.dart';

part 'providers.g.dart';

// Core Providers
@riverpod
SupabaseClient supabaseClient(SupabaseClientRef ref) {
  return Supabase.instance.client;
}

@riverpod
ScaleService scaleService(ScaleServiceRef ref) {
  return ScaleService();
}

@riverpod
PrinterService printerService(PrinterServiceRef ref) {
  return PrinterService();
}

// Repository Providers
@riverpod
AuthRepository authRepository(AuthRepositoryRef ref) {
  final supabase = ref.read(supabaseClientProvider);
  return AuthRepositoryImpl(
    remoteDataSource: AuthRemoteDataSourceImpl(supabase),
    localDataSource: AuthLocalDataSourceImpl(),
  );
}

@riverpod
SkuRepository skuRepository(SkuRepositoryRef ref) {
  final supabase = ref.read(supabaseClientProvider);
  return SkuRepositoryImpl(
    remoteDataSource: SkuRemoteDataSourceImpl(supabase),
    localDataSource: SkuLocalDataSourceImpl(),
  );
}

@riverpod
WeighingRepository weighingRepository(WeighingRepositoryRef ref) {
  final supabase = ref.read(supabaseClientProvider);
  return WeighingRepositoryImpl(
    remoteDataSource: WeighingRemoteDataSourceImpl(supabase),
    localDataSource: WeighingLocalDataSourceImpl(),
  );
}

// UseCase Providers
@riverpod
LoginUseCase loginUseCase(LoginUseCaseRef ref) {
  return LoginUseCase(ref.read(authRepositoryProvider));
}

@riverpod
GetSkuListUseCase getSkuListUseCase(GetSkuListUseCaseRef ref) {
  return GetSkuListUseCase(ref.read(skuRepositoryProvider));
}

@riverpod
CreateWeighingTransactionUseCase createWeighingTransactionUseCase(
  CreateWeighingTransactionUseCaseRef ref,
) {
  return CreateWeighingTransactionUseCase(ref.read(weighingRepositoryProvider));
}
```

### Main App Setup:

```dart
void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  
  await Supabase.initialize(
    url: 'your-supabase-url',
    anonKey: 'your-supabase-anon-key',
  );
  
  runApp(
    ProviderScope(
      child: MyApp(),
    ),
  );
}
```

---

## 🧪 Testing Structure (Riverpod)

```
test/
├── unit/
│   ├── core/
│   │   └── utils/
│   └── features/
│       ├── auth/
│       │   ├── providers/
│       │   └── usecases/
│       ├── sku/
│       │   ├── providers/
│       │   └── usecases/
│       ├── weighing/
│       │   ├── providers/
│       │   └── usecases/
│       └── reports/
│           ├── providers/
│           └── usecases/
├── widget/
│   ├── auth/
│   ├── sku/
│   ├── weighing/
│   └── shared/
├── integration/
│   ├── auth_flow_test.dart
│   ├── weighing_flow_test.dart
│   └── report_generation_test.dart
└── mocks/
    ├── mock_repositories.dart
    ├── mock_services.dart
    ├── mock_providers.dart
    └── test_data.dart
```

### Provider Testing Example:

```dart
void main() {
  group('WeighingNotifier', () {
    late ProviderContainer container;
    late MockSkuRepository mockSkuRepository;

    setUp(() {
      mockSkuRepository = MockSkuRepository();
      container = ProviderContainer(
        overrides: [
          skuRepositoryProvider.overrideWithValue(mockSkuRepository),
        ],
      );
    });

    tearDown(() {
      container.dispose();
    });

    test('should load SKU successfully', () async {
      // Arrange
      final sku = Sku(id: '1', name: 'Test SKU');
      when(() => mockSkuRepository.getSkuById(any()))
          .thenAnswer((_) async => sku);

      // Act
      await container.read(weighingNotifierProvider.notifier).loadSku('1');

      // Assert
      final state = container.read(weighingNotifierProvider);
      expect(state, isA<WeighingLoaded>());
      expect((state as WeighingLoaded).selectedSku, equals(sku));
    });
  });
}
```

---

## 🚀 Key Features Implementation (Riverpod)

### 1. **Scale Integration with Real-time Updates**
```dart
@riverpod
class ScaleNotifier extends _$ScaleNotifier {
  @override
  ScaleState build() {
    return const ScaleState.disconnected();
  }

  Stream<double> get weightStream {
    final scaleService = ref.read(scaleServiceProvider);
    return scaleService.weightStream;
  }

  Future<void> connectScale(ScaleConfig config) async {
    state = const ScaleState.connecting();
    try {
      final scaleService = ref.read(scaleServiceProvider);
      await scaleService.connectScale(config);
      state = const ScaleState.connected();
      
      // Listen to weight changes
      weightStream.listen((weight) {
        ref.read(currentWeightProvider.notifier).state = weight;
      });
    } catch (e) {
      state = ScaleState.error(e.toString());
    }
  }
}

final currentWeightProvider = StateProvider<double>((ref) => 0.0);
```

### 2. **QR Code Scanning with State Updates**
```dart
@riverpod
class QrScannerNotifier extends _$QrScannerNotifier {
  @override
  QrScannerState build() {
    return const QrScannerState.idle();
  }

  void onQrScanned(String qrData) {
    state = const QrScannerState.processing();
    
    try {
      // Parse QR data (could be SKU ID or Container ID)
      if (qrData.startsWith('SKU:')) {
        final skuId = qrData.substring(4);
        ref.read(weighingNotifierProvider.notifier).loadSku(skuId);
      } else if (qrData.startsWith('CONTAINER:')) {
        final containerId = qrData.substring(10);
        ref.read(weighingNotifierProvider.notifier).loadContainer(containerId);
      }
      
      state = QrScannerState.success(qrData);
    } catch (e) {
      state = QrScannerState.error(e.toString());
    }
  }
}
```

### 3. **Label Printing with Queue Management**
```dart
@riverpod
class PrintingNotifier extends _$PrintingNotifier {
  @override
  PrintingState build() {
    return const PrintingState.idle();
  }

  Future<void> printLabel(LabelData labelData) async {
    state = const PrintingState.printing();
    
    try {
      final printerService = ref.read(printerServiceProvider);
      await printerService.printLabel(labelData);
      
      // Update transaction as printed
      final weighingNotifier = ref.read(weighingNotifierProvider.notifier);
      await weighingNotifier.markLabelPrinted(labelData.transactionId);
      
      state = const PrintingState.success();
    } catch (e) {
      state = PrintingState.error(e.toString());
    }
  }
}
```

### 4. **Real-time Sync with Supabase**
```dart
@riverpod
Stream<List<WeighingTransaction>> realtimeTransactions(
  RealtimeTransactionsRef ref,
) {
  final supabase = ref.read(supabaseClientProvider);
  
  return supabase
      .from('weighing_transaction')
      .stream(primaryKey: ['id'])
      .order('created_at', ascending: false)
      .limit(50)
      .map((data) => data
          .map((json) => WeighingTransaction.fromJson(json))
          .toList());
}

// Auto-refresh dashboard when new transactions come in
@riverpod
class DashboardNotifier extends _$DashboardNotifier {
  @override
  DashboardState build() {
    // Listen to real-time transactions
    ref.listen(realtimeTransactionsProvider, (previous, next) {
      next.when(
        data: (transactions) {
          // Update dashboard stats when new data arrives
          _updateDashboardStats(transactions);
        },
        loading: () {},
        error: (error, stack) {},
      );
    });
    
    return const DashboardState.loading();
  }
  
  void _updateDashboardStats(List<WeighingTransaction> transactions) {
    // Calculate stats and update state
    final todayTransactions = transactions
        .where((t) => _isToday(t.dateTime))
        .length;
    
    state = DashboardState.loaded(
      todayTransactions: todayTransactions,
      totalWeight: _calculateTotalWeight(transactions),
      qcAlerts: _getQcAlerts(transactions),
    );
  }
}
```

---

## 📱 Screen Flow

```
Splash → Login → Dashboard
                    ├── Weighing Flow
                    │   ├── SKU Selection
                    │   ├── Container Selection
                    │   ├── Weight Reading
                    │   ├── QC Check
                    │   ├── Data Input
                    │   └── Save & Print
                    ├── Reports
                    │   ├── Transaction History
                    │   ├── Charts & Analytics
                    │   └── Export Options
                    ├── Settings
                    │   ├── Scale Configuration
                    │   ├── Printer Settings
                    │   ├── QC Configuration
                    │   └── User Management
                    └── Profile
```

---

## 🔧 Development Guidelines

### 1. **Code Organization**
- ✅ One feature per folder
- ✅ Separate presentation, domain, and data layers
- ✅ Use barrel exports (index.dart files)
- ✅ Follow naming conventions

### 2. **State Management**
- ✅ Use Riverpod for reactive state management
- ✅ Use StateNotifier for complex business logic
- ✅ Use Provider/FutureProvider for data fetching
- ✅ Keep UI widgets pure (no business logic)

### 3. **Error Handling**
- ✅ Centralized error handling
- ✅ User-friendly error messages
- ✅ Proper exception hierarchy

### 4. **Performance**
- ✅ Lazy loading for large lists
- ✅ Image caching for better UX
- ✅ Debouncing for search inputs
- ✅ Connection pooling for database

### 5. **Testing**
- ✅ Unit tests for business logic
- ✅ Widget tests for UI components
- ✅ Integration tests for critical flows
- ✅ Mock external dependencies

---

## 🎯 Next Development Steps

1. **Setup Project Structure** (Day 1-2)
   - Initialize Flutter project
   - Setup folder structure
   - Configure dependencies
   - Setup routing

2. **Core Services** (Day 3-4)
   - Supabase integration
   - Dependency injection
   - Error handling
   - Theme configuration

3. **Authentication Module** (Day 5-6)
   - Login/logout functionality
   - User session management
   - Role-based access

4. **Begin Feature Development** (Day 7+)
   - Start with SKU management
   - Then container management
   - Follow with weighing workflow

This structure provides a solid foundation for scalable, maintainable Flutter application development! 🚀
