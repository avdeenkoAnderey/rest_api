from fastapi import FastAPI, HTTPException, Query
from app.models import AdvertisementCreate, AdvertisementUpdate, AdvertisementResponse
from app.database import db

app = FastAPI(title="Advertisement Service")


@app.post("/advertisement", response_model=AdvertisementResponse, status_code=201)
def create_advertisement(ad: AdvertisementCreate):
    return db.create(ad.title, ad.description, ad.price, ad.author)


@app.get("/advertisement/{advertisement_id}", response_model=AdvertisementResponse)
def get_advertisement(advertisement_id: int):
    advertisement = db.get_by_id(advertisement_id)
    if advertisement is None:
        raise HTTPException(status_code=404, detail="Advertisement not found")
    return advertisement


@app.patch("/advertisement/{advertisement_id}", response_model=AdvertisementResponse)
def update_advertisement(advertisement_id: int, ad: AdvertisementUpdate):
    updated = db.update(advertisement_id, title=ad.title, description=ad.description, price=ad.price, author=ad.author)
    if updated is None:
        raise HTTPException(status_code=404, detail="Advertisement not found")
    return updated


@app.delete("/advertisement/{advertisement_id}", status_code=204)
def delete_advertisement(advertisement_id: int):
    if not db.delete(advertisement_id):
        raise HTTPException(status_code=404, detail="Advertisement not found")


@app.get("/advertisement", response_model=list[AdvertisementResponse])
def search_advertisements(
    title: str | None = Query(None),
    description: str | None = Query(None),
    author: str | None = Query(None),
    price_min: float | None = Query(None),
    price_max: float | None = Query(None),
    date_from: str | None = Query(None),
    date_to: str | None = Query(None),
):
    results = db.search(
        title=title,
        description=description,
        author=author,
        price_min=price_min,
        price_max=price_max,
        date_from=date_from,
        date_to=date_to,
    )
    return results
