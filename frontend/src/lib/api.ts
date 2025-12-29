const BASE_URL = 'http://localhost:2468';

/**
 * Standard API wrapper for Hyperion with an integrated silent refresh mechanism.
 * * :param endpoint: The target URL fragment.
 * :param options: Standard fetch configuration.
 * :returns: The parsed JSON response.
 */
export async function api<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
    const url = `${BASE_URL}${endpoint}`;
    
    options.credentials = 'include'; // Ensure cookies are always sent
    options.headers = {
        'Content-Type': 'application/json',
        ...options.headers,
    };

    let response = await fetch(url, options);

    // If the access_token is expired (401), we attempt a silent refresh
    if (response.status === 401 && endpoint !== '/api/accounts/login') {
        console.log("Access token expired. Attempting silent refresh...");

        const refreshResponse = await fetch(`${BASE_URL}/api/accounts/refresh`, {
            method: 'POST',
            credentials: 'include'
        });

        if (refreshResponse.ok) {
            console.log("Refresh successful. Retrying original request.");
            // Retry the original request with the new cookies now present in the browser
            response = await fetch(url, options);
        } else {
            console.warn("Refresh failed. Session is invalid.");
            // If the refresh fails, the user must log in again
            throw new Error("UNAUTHORISED");
        }
    }

    if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `API Error: ${response.statusText}`);
    }

    return response.json();
}