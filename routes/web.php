use App\Http\Controllers\InventoryController;

Route::get('/api/search', [InventoryController::class, 'search'])->name('api.search');