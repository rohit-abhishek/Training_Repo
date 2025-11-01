#include <cstdio>
#include <chrono>
#include <cstdint>

static inline double calculate(int iterations, int param1, int param2) noexcept {
    double result = 1.0;
#if defined(__clang__)
#pragma clang loop vectorize(disable)
#pragma clang loop unroll(enable)
// #pragma clang loop unroll_count(8)
#endif
    for (int i = 1; i <= iterations; ++i) {
        int t = i * param1;
        result -= 1.0 / static_cast<double>(t - param2);
        result += 1.0 / static_cast<double>(t + param2);
    }
    return result;
}

int main() {
    using clock = std::chrono::steady_clock;
    auto start_time = clock::now();

    double result = calculate(200000000, 4, 1) * 4.0;

    auto end_time = clock::now();
    double elapsed = std::chrono::duration<double>(end_time - start_time).count();

    std::printf("Result: %.12f\n", result);
    std::printf("Execution Time: %.6f seconds\n", elapsed);
    return 0;
}