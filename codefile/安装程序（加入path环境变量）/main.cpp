#include <windows.h>
#include <string>
#include <direct.h>
#include <bits/stdc++.h>
std::string current_working_directory()
{
	char buff[250];
	_getcwd(buff, 250); 
	std::string current_working_directory(buff);
	return current_working_directory;
}
std::wstring string_to_wstring(const std::string& str) {
	int size = MultiByteToWideChar(CP_UTF8, 0, str.c_str(), -1, NULL, 0);
	std::wstring wstr(size, 0);
	MultiByteToWideChar(CP_UTF8, 0, str.c_str(), -1, &wstr[0], size);
	return wstr;
}
bool add_to_system_path(const std::wstring& path) {
	HKEY hKey;
	if (RegOpenKeyExW(
		HKEY_LOCAL_MACHINE,
		L"SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Environment",
		0,
		KEY_ALL_ACCESS,
		&hKey
		) != ERROR_SUCCESS) {
		return false;
	}
	wchar_t oldPath[32767];
	DWORD size = sizeof(oldPath);
	if (RegQueryValueExW(hKey, L"PATH", NULL, NULL, (LPBYTE)oldPath, &size) != ERROR_SUCCESS) {
		RegCloseKey(hKey);
		return false;
	}
	std::wstring newPath = std::wstring(oldPath) + L";" + path;
	if (RegSetValueExW(
		hKey,
		L"PATH",
		0,
		REG_EXPAND_SZ,
		(const BYTE*)newPath.c_str(),
		(newPath.size() + 1) * sizeof(wchar_t)
		) != ERROR_SUCCESS) {
		RegCloseKey(hKey);
		return false;
	}
	
	RegCloseKey(hKey);
	SendMessageTimeoutW(HWND_BROADCAST, WM_SETTINGCHANGE, 0, (LPARAM)L"Environment", SMTO_ABORTIFHUNG, 5000, NULL);
	return true;
}
int main() {
	std::string path = current_working_directory();
	std::wstring wpath = string_to_wstring(path);
	if (add_to_system_path(wpath)) {
		std::cout << "PATH updated successfully." << std::endl;
	} else {
		std::cerr << "Failed to update PATH." << std::endl;
	}
	return 0;
}
