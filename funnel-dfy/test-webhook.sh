#!/usr/bin/env bash
# Manda un payload de prueba (mismo formato que el quiz) al Inbound Webhook
# de GHL, para poder hacer "Fetch sample request" y mapear en el workflow.
curl -sS -w "\nHTTP %{http_code}\n" -X POST \
  'https://services.leadconnectorhq.com/hooks/zos8yS6edLzzrWczWWHh/webhook-trigger/29facbf5-f915-46ce-afba-2db10a3e2a33' \
  -H 'Content-Type: application/json' \
  -d '{"firstName":"Prueba","fullName":"Prueba Test","email":"prueba.test@flowscale.com","phone":"+15555550123","empresa":"Empresa Prueba LLC","facturacion":"$5,000 a $10,000","clientes":"6 a 15 clientes","obstaculo":"No genero suficientes oportunidades calificadas","timeline":"Solo estoy explorando opciones","valorEstimado":7500,"califica":"si","prioridad":"explorando","source":"index-dfy-reparadores-credito"}'
