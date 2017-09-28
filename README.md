# Progetto-Ricerca-Operativa

## Gestione di un ambulatorio - Open shop

Un ambulatorio fornisce un insieme di Test T={t1,..,t5} ai suoi pazienti. 
Ogni test richiede un tempo diverso d1,..d5. In ogni giornata, ciascun paziente pP viene ammesso in 
una delle 3 salette disponibili (identiche) e viene sottoposto a tutti gli esami da lui richiesti T(p)T, 
e solo al termine esce dalla saletta. Ogni esame è svolto da un operatore specializzato che può seguire un paziente
alla volta e si trattiene con esso per tutta la durata dell’esame. Noto P e avendo 2 operatori per ogni test, determinare 
a che ora deve presentarsi ciascun paziente affinchè il makespan dell’intero processo sia minimo.


###### Decisioni:
1. Pazienti inseriti nelle salette in due modi:
   - Per ordine di arrivo (1-2-3-4-5....)
   - Secondo First Fit Decreasing

2. Pazienti eseguono prima i test più LUNGHI
