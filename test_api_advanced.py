#!/usr/bin/env python3
"""
Script de prueba avanzado para la API de usuarios
"""

import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def test_update_user():
    """Prueba PUT /api/users/{id}"""
    print("Testing PUT /api/users/27...")
    update_data = {
        "NOMBRE_COMPLETO": "JO-Maria Garcia Lopez Actualizada",
        "EMAIL": "maria.updated@empresa.com"
    }
    
    response = requests.put(
        f"{BASE_URL}/api/users/27",
        json=update_data,
        headers={"Content-Type": "application/json"}
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()

def test_delete_user_soft():
    """Prueba DELETE /api/users/{id} (soft delete)"""
    print("Testing DELETE /api/users/28 (soft delete)...")
    response = requests.delete(f"{BASE_URL}/api/users/28")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()

def test_search_with_filters():
    """Prueba GET /api/users/search con filtros"""
    print("Testing GET /api/users/search with filters...")
    response = requests.get(f"{BASE_URL}/api/users/search?q=JO&area=DISENO&limit=5")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()

def test_get_users_with_filters():
    """Prueba GET /api/users con filtros"""
    print("Testing GET /api/users with filters...")
    response = requests.get(f"{BASE_URL}/api/users?area=DISENO&limit=10")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()

def test_create_duplicate_user():
    """Prueba POST /api/users con código duplicado"""
    print("Testing POST /api/users with duplicate code...")
    user_data = {
        "CODIGO_USUARIO": "TEST001",  # Este ya existe
        "NOMBRE_COMPLETO": "Usuario Duplicado",
        "EMAIL": "duplicate@empresa.com",
        "AREA": "DISEÑO",
        "ROL": "DISEÑADOR"
    }
    
    response = requests.post(
        f"{BASE_URL}/api/users",
        json=user_data,
        headers={"Content-Type": "application/json"}
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()

def test_get_nonexistent_user():
    """Prueba GET /api/users/{id} con ID inexistente"""
    print("Testing GET /api/users/999...")
    response = requests.get(f"{BASE_URL}/api/users/999")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()

if __name__ == "__main__":
    print("=== Pruebas Avanzadas de la API de Usuarios ===\n")
    
    test_get_users_with_filters()
    test_search_with_filters()
    test_update_user()
    test_delete_user_soft()
    test_create_duplicate_user()
    test_get_nonexistent_user()
    
    print("=== Pruebas avanzadas completadas ===")