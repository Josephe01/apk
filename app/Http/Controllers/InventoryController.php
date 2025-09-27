namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Models\InventoryItem;

class InventoryController extends Controller
{
    /**
     * Search for a product by barcode or SKU.
     */
    public function search(Request $request)
    {
        $query = $request->input('query');

        // Validate the input
        if (!$query) {
            return response()->json(['success' => false, 'message' => 'Query is required'], 400);
        }

        // Search the database
        $product = InventoryItem::where('barcode', $query)
            ->orWhere('sku', $query)
            ->first();

        if ($product) {
            return response()->json(['success' => true, 'product' => $product]);
        }

        return response()->json(['success' => false, 'message' => 'Product not found'], 404);
    }
}