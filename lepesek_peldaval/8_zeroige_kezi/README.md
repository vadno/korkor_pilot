Ebben a lépésben az esetleges tokenizálási hibák javítása mellett a zéró létigék és az elliptált igék kézi beillesztése történik. Ehhez az [UD Annotatrix](https://github.com/jonorthwash/ud-annotatrix) eszközt használjuk, amely egy böngészőben használható eszköz függőségi fák vizualizációjára és szerkesztésére.

A zéró létigék új tokenként kerülnek a fájlba arra a helyre, ahol múlt időben testes létigeként jelennének meg, saját kombinált indexet kapnak, ami a zéró létigét megelőző elem ID-jéből képződik. Az igei ellipsziseket is jelöltük a korpuszban, hiszen gyakran találkoztunk olyan tagmondatokkal, amelyekben az elliptált ige miatt nem lehetett megfelelő anyacsomóponthoz kötni az egyes bővítményeket. A zéró létigékhez hasonlóan kézzel illesztettük a mondatfába az elliptált finit igéket. Az elliptált ige a zéró létigéhez hasonló, kombinált indexet kapott.

A részleteket lásd az [annotálási útmutatóban](../../utmutatok/zero_verb_guide.pdf)!

A lépés bemenete: [7_webanno_kezi/globv_10.conll](../7_webanno_kezi/globv_10.conll)
